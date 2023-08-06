import os
import time
from asyncio import AbstractEventLoop

from consul.aio import Consul as AioConsul
from aioch import Client as ClickhouseAioClient

from singleton_decorator import singleton
import hvac
import consulate
import json
import clickhouse_driver as ch_d
from kafka import KafkaProducer, KafkaConsumer
from azure.storage.blob import BlobClient, ContainerClient
import logging_loki
import logging
import functools
import datetime
import aiokafka
from ssl import SSLContext
import traceback
import psycopg2
import aioboto3
import boto3
from prometheus_client import \
    CollectorRegistry, Counter, Gauge, Summary, \
    push_to_gateway, write_to_textfile, start_http_server, exposition
import redis
from redis import asyncio as aioredis
from clickhouse_pool import ChPool


@singleton
class Prometheus:
    registry = None  # type: CollectorRegistry
    gauge_instances = {}

    def __init__(self):
        self.registry = CollectorRegistry()

    def get_registry(self) -> CollectorRegistry:
        return self.registry

    def start_server(self, **kwargs) -> None:
        port = 4000 if not 'port' in kwargs else kwargs['port']

        start_http_server(port=port, registry=self.registry)

    def counter(self, name: str, documentation: str) -> Counter:
        return Counter(name, documentation, registry=self.registry)

    def gauge(self, **kwargs) -> Gauge:
        r"""
            :Keyword Arguments:
                * *new* (``boolean``) --
                  Return force new object
                * *name* (``str``) --
                  Name of Gauge
                * *documentation* (``str``) --
                  Documentation of Gauge
            """
        if 'new' in kwargs:
            return Gauge(kwargs['name'], kwargs['documentation'], registry=self.registry)

        if kwargs['name'] not in self.gauge_instances:
            self.gauge_instances[kwargs['name']] = Gauge(kwargs['name'], kwargs['documentation'],
                                                         registry=self.registry)

        return self.gauge_instances[kwargs['name']]

    def summary(self, name: str, documentation: str) -> Summary:
        return Summary(name, documentation, registry=self.registry)

    def push_to_gateway(self, gateway: str, job: str) -> None:
        push_to_gateway(gateway=gateway, job=job, registry=self.registry)

    def write_to_textfile(self, file: str) -> None:
        write_to_textfile(file, self.registry)

    def get_output(self) -> str:
        return exposition.generate_latest(self.get_registry())


def log(_func=None, *, logger = None):
    def decorator_dvglog(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if logger is None:
                cust_logger = logging.Logger(__name__)
                sh = logging.StreamHandler()
                sh.setLevel(logging.DEBUG)
                formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                sh.setFormatter(formatter)
                cust_logger.addHandler(sh)
                try:
                    factory = Factory()
                    l_h = factory.loki_handler(tags={"application": "log-decorator"}, version="1")
                    l_h.setLevel(logging.DEBUG)
                    l_h.setFormatter(formatter)
                    cust_logger.addHandler(l_h)
                except:
                    pass
            else:
                cust_logger = logger
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)
            cust_logger.debug(f"function {func.__name__} called with args {signature}")
            try:
                tst = datetime.datetime.utcnow()
                result = func(*args, **kwargs)
                cust_logger.debug(f"Work time of function {func.__name__} = {datetime.datetime.utcnow() - tst}")
                return result
            except Exception as e:
                trcbk = traceback.format_exc()
                cust_logger.exception(f"Exception raised in {func.__name__}. exception: {str(e)}. {trcbk}")
                raise e
        return wrapper
    if _func is None:
        return decorator_dvglog
    else:
        return decorator_dvglog(_func)


def retry(_func=None, *, num_retry = 1, sleep_s = 0.1):
    def decorator_retry(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            cnt = num_retry
            while True:
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    cnt -= 1
                    if cnt <=0:
                        raise e
                    if sleep_s > 0:
                        time.sleep(sleep_s)
        return wrapper
    if _func is None:
        return decorator_retry
    else:
        return decorator_retry(_func)

logger = logging.getLogger(__name__)

consul_keys = {"clickhouse": "env/databases/clickhouse", "kafka": "env/databases/kafka",
               "ms-azure-se": "env/databases/ms-azure-se", "loki": "env/databases/loki",
               "greenplum": "env/databases/greenplum", "storage": "env/databases/storage",
               "redis": "env/databases/redis"}
services = {
    "consul": {},
    "aio_consul": {},

    "kafka_producer": {},
    "kafka_consumer": {},
    "aiokafka_producer": {},
    "aiokafka_consumer": {},

    "clickhouse_client": {},
    "clickhouse_pool": {},
    "aio_clickhouse": {},

    "azure_container_client": {},
    "azure_blob_client": {},

    "loki_handler": {},

    "gp_connection": {},
    "prometheus": {},

    "aiostorage_client": {},
    "aiostorage_resource": {},
    "storage_client": {},
    "storage_resource": {},
    "redis_client": {},
    "aioredis_client": {}
}


@singleton
class Factory:
    def_instance_name = "default"
    key_new = "new"
    key_istance_name = "instance_name"
    def __init__(self, vault_url=None, vault_token=None):
        self.__consul_keys = consul_keys
        self.__services = services
        if vault_url is None:
            self.vault_url = os.getenv("VAULT_URL")
        else:
            self.vault_url = vault_url
        if vault_token is None:
            self.vault_token = os.getenv("VAULT_TOKEN")
        else:
            self.vault_token = vault_token
        self.vault = self.vault_client(url=self.vault_url, token=self.vault_token)
        self.secrets = self.init_secrets()
        self.config = self.init_config()

    def info(self) -> str:
        s = "Класс Factory\n"
        s += 'Создание экземпляра:\n ins = Factory(vault_url=url, vault_token=token)\n'
        s += "Методы: \n" + "1 ins.vault_client(url: str, token: str)\n"
        for i, k in enumerate(self.__services.keys()):
            s += str(i+2)+" "+"ins."+k +"(**kwargs)\n"
        s += "Для создания нового экземпляра укажите в kwargs: new=True\n"
        s += "Для создания именнованного экземпляра укажите в kwargs: instance_name='Имя экземпляра'\n"
        s += "\n"
        s += "Пути настроек в consul:\n"
        s += json.dumps(self.__consul_keys)
        return s

    def init_secrets(self) -> dict:
        rs = {}
        for service in list(self.__consul_keys.keys())+["consul"]:
            rs[service] = self._get_secrets(service)
        return rs

    def init_config(self) -> dict:
        rs = {}
        for service in self.__consul_keys.keys():
            rs[service] = self.get_config_from_consul(service)
        return rs

    def delete_from_kwargs(self, kwargs):
        if self.key_new in kwargs:
            del kwargs[self.key_new]
        if self.key_istance_name in kwargs:
            del kwargs[self.key_istance_name]
        return kwargs

    def get_instance(self, service_builder, service_name, instance_name, args=[], kwargs={}):
        if (self.key_new in kwargs) and (not kwargs[self.key_new]) and (instance_name in self.__services[service_name]):
            return self.__services[service_name][instance_name]
        #if ((self.key_new in kwargs) and kwargs[self.key_new]) or not(instance_name in self.__services[service_name]):
        kwargs = self.delete_from_kwargs(kwargs)
        inst = service_builder(*args, **kwargs)
        self.__services[service_name][instance_name] = inst
        return self.__services[service_name][instance_name]

    def vault_client(self, url: str, token: str) -> hvac.Client:
        vault = hvac.Client(url=url, token=token)
        return vault

    def _get_secrets(self, service: str) -> dict:
        ret = self.vault.secrets.kv.v2.read_secret_version(path=service)["data"]["data"]
        return ret

    def get_config_from_consul(self, service) -> dict:
        cnsl = self.consul(instance_name="in_uses_for_factory")
        config = cnsl.kv[self.__consul_keys[service]]
        config = json.loads(config)
        return config

    def consul(self, **kwargs) -> consulate.Consul:
        instance_name = self.def_instance_name if not self.key_istance_name in kwargs else kwargs[self.key_istance_name]
        return self._consul_client(consulate.Consul, "consul", instance_name, kwargs)

    def aio_consul(self, **kwargs) -> AioConsul:
        r"""Create and return object of async consul client
            :Keyword Arguments:
                * *loop* (``AbstractEventLoop``) --
                  Custom event loop
            """
        instance_name = self.def_instance_name if not self.key_istance_name in kwargs else kwargs[self.key_istance_name]
        return self._consul_client(AioConsul, "aio_consul", instance_name, kwargs)

    def _consul_client(self, service_builder, service_name: str, instance_name: str, kwargs):
        secrets = self.secrets["consul"]

        kwargs["host"] = secrets["url"] if not "url" in kwargs else kwargs["url"]
        kwargs["port"] = secrets["port"] if not "port" in kwargs else kwargs["port"]
        kwargs["token"] = secrets["backend_token"] if not "token" in kwargs else kwargs["token"]

        return self.get_instance(service_builder, service_name, instance_name, [], kwargs)


    def _get_clickhouse_kwargs(self, kwargs):
        ch_type = None if not "type" in kwargs else kwargs["type"]
        secrets = self._get_clickhouse_secrets(ch_type)
        config = self._get_clickhouse_config(ch_type)
        if "type" in kwargs.keys():
            del kwargs["type"]
        kwargs["host"] = config["url"] if not ("host" in kwargs) else kwargs["host"]
        kwargs["host"] = kwargs["host"] if not ("url" in kwargs) else kwargs["url"]
        kwargs["port"] = config["port"] if not ("port" in kwargs) else kwargs["port"]
        kwargs["user"] = secrets["user"] if not ("user" in kwargs) else kwargs["user"]
        kwargs["password"] = secrets["password"] if not ("password" in kwargs) else kwargs["password"]
        kwargs["secure"] = True if "secure" not in kwargs else kwargs["secure"]
        kwargs["verify"] = False if "verify" not in kwargs else kwargs["verify"]
        return kwargs


    def clickhouse_pool(self, **kwargs) -> ChPool:
        service_name = "clickhouse_pool"
        instance_name = self.def_instance_name if not self.key_istance_name in kwargs else kwargs[self.key_istance_name]
        kwargs = self._get_clickhouse_kwargs(kwargs)
        args = []
        return self.get_instance(ChPool, service_name, instance_name, args, kwargs)



    def clickhouse_client(self, **kwargs) -> ch_d.Client:
        r"""Create and return object of clickhouse client
            :Keyword Arguments:
                * *type* (``str``) -- postfix for secret and config name (clickhouse_TYPE). Default: None (clickhouse)
            """
        service_name = "clickhouse_client"
        instance_name = self.def_instance_name if not self.key_istance_name in kwargs else kwargs[self.key_istance_name]
        kwargs = self._get_clickhouse_kwargs(kwargs)
        args = []
        return self.get_instance(ch_d.Client, service_name, instance_name, args, kwargs)

    def aio_clickhouse(self, loop: AbstractEventLoop, **kwargs) -> ClickhouseAioClient:
        r"""Create and return object of clickhouse client
            :Keyword Arguments:
                * *type* (``str``) -- postfix for secret and config name (clickhouse_TYPE). Default: None (clickhouse)
            """
        service_name = "aio_clickhouse"
        instance_name = self.def_instance_name if not self.key_istance_name in kwargs else kwargs[self.key_istance_name]

        ch_type = None if not "type" in kwargs else kwargs["type"]
        secrets = self._get_clickhouse_secrets(ch_type)
        config = self._get_clickhouse_config(ch_type)

        if "type" in kwargs.keys():
            del kwargs["type"]

        args = []
        args.append(config["url"] if "url" not in kwargs else kwargs["url"])

        kwargs["port"] = config["port"] if not ("port" in kwargs) else kwargs["port"]
        kwargs["user"] = secrets["user"] if not ("user" in kwargs) else kwargs["user"]
        kwargs["password"] = secrets["password"] if not ("password" in kwargs) else kwargs["password"]
        kwargs["secure"] = True if "secure" not in kwargs else kwargs["secure"]
        kwargs["verify"] = False if "verify" not in kwargs else kwargs["verify"]

        kwargs["loop"] = loop

        return self.get_instance(ClickhouseAioClient, service_name, instance_name, args, kwargs)

    def _get_clickhouse_secrets(self, ch_type: str = None) -> dict:
        if ch_type is None or ch_type == "":
            return self.secrets["clickhouse"]

        if f"clickhouse_{ch_type}" not in self.secrets:
            self.secrets[f"clickhouse_{ch_type}"] = self._get_secrets(f"clickhouse_{ch_type}")

        return self.secrets[f"clickhouse_{ch_type}"]

    def _get_clickhouse_config(self, ch_type: str = None) -> dict:
        if ch_type is None or ch_type == "":
            return self.config["clickhouse"]

        if f"clickhouse_{ch_type}" not in self.config:
            consul = self.consul(instance_name="in_uses_for_factory")
            consul_config = consul.kv[f"env/databases/clickhouse_{ch_type}"]
            self.config[f"clickhouse_{ch_type}"] = json.loads(consul_config)

        return self.config[f"clickhouse_{ch_type}"]

    def kafka_producer(self, **kwargs) -> KafkaProducer:
        def serialiser(v):
            return json.dumps(v).encode('utf-8')
        service_name = "kafka_producer"
        instance_name = self.def_instance_name if not self.key_istance_name in kwargs else kwargs[self.key_istance_name]
        scrts = self.secrets["kafka"]
        cnfg = self.config["kafka"]
        if "ssl_cafile" not in kwargs:
            filename = os.getcwd() + service_name+"_"+instance_name+".pem"
            if not os.path.exists(filename):
                with open(filename, "w") as f:
                    pass
                    f.write(scrts["pem"])
            kwargs["ssl_cafile"] = filename
        kwargs["value_serializer"] = serialiser if not ("value_serializer" in kwargs) else kwargs["value_serializer"]
        kwargs["bootstrap_servers"] = cnfg["url"] if "url" not in kwargs else kwargs["url"]
        kwargs["security_protocol"] = "SSL" if "security_protocol" not in kwargs else kwargs["security_protocol"]
        return self.get_instance(KafkaProducer, service_name, instance_name, [], kwargs)

    def aiokafka_producer(self, **kwargs) -> aiokafka.AIOKafkaProducer:
        def serialiser(v):
            return json.dumps(v).encode('utf-8')
        service_name = "aiokafka_producer"
        instance_name = self.def_instance_name if not self.key_istance_name in kwargs else kwargs[self.key_istance_name]
        scrts = self.secrets["kafka"]
        cnfg = self.config["kafka"]
        if "ssl_context" not in kwargs:
            filename = os.getcwd() + service_name+"_"+instance_name+".pem"
            if not os.path.exists(filename):
                with open(filename, "w") as f:
                    pass
                    f.write(scrts["pem"])
            ssl_context = SSLContext()
            ssl_context.load_verify_locations(capath=filename)
            kwargs["ssl_context"] = ssl_context
        kwargs["value_serializer"] = serialiser if "value_serializer" not in kwargs else kwargs["value_serializer"]
        kwargs["bootstrap_servers"] = cnfg["url"] if "url" not in kwargs else kwargs["url"]
        kwargs["security_protocol"] = "SSL" if "security_protocol" not in kwargs else kwargs["security_protocol"]
        return self.get_instance(aiokafka.AIOKafkaProducer, service_name, instance_name, [], kwargs)


    def kafka_consumer(self, *args, **kwargs) -> KafkaConsumer:
        def value_deserializer(m):
            return json.loads(m.decode('ascii'))
        service_name = "kafka_consumer"
        instance_name = self.def_instance_name if not self.key_istance_name in kwargs else kwargs[self.key_istance_name]
        scrts = self.secrets["kafka"]
        cnfg = self.config["kafka"]
        if "ssl_cafile" not in kwargs:
            filename = os.getcwd() + service_name+"_"+instance_name+".pem"
            if not os.path.exists(filename):
                with open(filename, "w") as f:
                    pass
                    f.write(scrts["pem"])
            kwargs["ssl_cafile"] = filename
        kwargs["bootstrap_servers"] = cnfg["url"] if "url" not in kwargs else kwargs["url"]
        kwargs["security_protocol"] = "SSL" if "security_protocol" not in kwargs else kwargs["security_protocol"]
        kwargs["value_deserializer"] = value_deserializer if "value_deserializer" not in kwargs else kwargs["value_deserializer"]
        return self.get_instance(KafkaConsumer, service_name, instance_name, args, kwargs)

    def aiokafka_consumer(self,*args, **kwargs) -> aiokafka.AIOKafkaConsumer:
        def value_deserializer(m):
            return json.loads(m.decode('utf-8'))
        service_name = "aiokafka_consumer"
        instance_name = self.def_instance_name if not self.key_istance_name in kwargs else kwargs[self.key_istance_name]
        scrts = self.secrets["kafka"]
        cnfg = self.config["kafka"]
        if "ssl_context" not in kwargs:
            filename = os.getcwd() + service_name+"_"+instance_name+".pem"
            if not os.path.exists(filename):
                with open(filename, "w") as f:
                    pass
                    f.write(scrts["pem"])
            ssl_context = SSLContext()
            ssl_context.load_verify_locations(capath=filename)
            kwargs["ssl_context"] = ssl_context
        kwargs["bootstrap_servers"] = cnfg["url"] if "url" not in kwargs else kwargs["url"]
        kwargs["security_protocol"] = "SSL" if "security_protocol" not in kwargs else kwargs["security_protocol"]
        kwargs["value_deserializer"] = value_deserializer if "value_deserializer" not in kwargs else kwargs["value_deserializer"]
        return self.get_instance(aiokafka.AIOKafkaConsumer, service_name, instance_name, args, kwargs)


    def azure_container_client(self,**kwargs) -> ContainerClient:
        service_name = "azure_container_client"
        instance_name = self.def_instance_name if not self.key_istance_name in kwargs else kwargs[self.key_istance_name]
        if "conn_str" not in kwargs:
            scrts = self.secrets["ms-azure-se"]
            cnfg = self.config["ms-azure-se"]
            account_name = scrts["AccountName"]
            account_key = scrts["AccountKey"]
            kwargs["conn_str"] = self.get_cs4azure(account_name, account_key)
        return self.get_instance(ContainerClient.from_connection_string, service_name, instance_name, [], kwargs)

    def azure_blob_client(self, **kwargs) -> BlobClient:
        service_name = "azure_blob_client"
        instance_name = self.def_instance_name if not self.key_istance_name in kwargs else kwargs[self.key_istance_name]
        if "conn_str" not in kwargs:
            scrts = self.secrets["ms-azure-se"]
            cnfg = self.config["ms-azure-se"]
            account_name = scrts["AccountName"]
            account_key = scrts["AccountKey"]
            kwargs["conn_str"] = self.get_cs4azure(account_name, account_key)
        return self.get_instance(BlobClient.from_connection_string, service_name, instance_name, [], kwargs)

    def get_cs4azure(self, account_name, account_key):
        cs = "DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net"
        cs += ";AccountName=" + account_name
        cs += ";AccountKey=" + account_key
        return cs

    def loki_handler(self, **kwargs) -> logging_loki.LokiHandler:
        service_name = "loki_handler"
        instance_name = self.def_instance_name if not self.key_istance_name in kwargs else kwargs[self.key_istance_name]
        scrts = self.secrets["loki"]
        cnfg = self.config["loki"]
        kwargs["url"] = cnfg["url"] if not "url" in kwargs else kwargs["url"]
        kwargs["auth"] = (scrts["user"], scrts["password"]) if not "auth" in kwargs else kwargs["auth"]
        return self.get_instance(logging_loki.LokiHandler, service_name, instance_name, [], kwargs)

    def gp_connection(self, **kwargs):
        service_name = "gp_connection"
        instance_name = self.def_instance_name if not self.key_istance_name in kwargs else kwargs[self.key_istance_name]
        scrts = self.secrets["greenplum"]
        cnfg = self.config["greenplum"]
        kwargs["host"] = cnfg["url"] if not "url" in kwargs else kwargs["url"]
        kwargs["user"] = scrts["user"] if not "user" in kwargs else kwargs["user"]
        kwargs["password"] = scrts["password"] if not "password" in kwargs else kwargs["password"]
        kwargs["port"] = cnfg["port"] if not "port" in kwargs else kwargs["port"]
        kwargs["dbname"] = cnfg["dbname"] if not "dbname" in kwargs else kwargs["dbname"]
        kwargs["target_session_attrs"] = cnfg["target_session_attrs"] if not "target_session_attrs" in kwargs else kwargs["target_session_attrs"]
        return self.get_instance(psycopg2.connect, service_name, instance_name, [], kwargs)

    def prometheus(self, **kwargs) -> Prometheus:
        service_name = "prometheus"
        instance_name = self.def_instance_name if not self.key_istance_name in kwargs else kwargs[self.key_istance_name]
        return self.get_instance(Prometheus, service_name, instance_name)

    def _storage_driver(self, f, service_name, kwargs):
        instance_name = self.def_instance_name if not self.key_istance_name in kwargs else kwargs[self.key_istance_name]
        scrts = self.secrets["storage"]
        cnfg = self.config["storage"]
        kwargs["service_name"] = "s3" if not "service_name" in kwargs else kwargs["service_name"]
        kwargs["endpoint_url"] = cnfg["url"] if not "url" in kwargs else kwargs["url"]
        kwargs["aws_access_key_id"] = scrts["aws_access_key_id"] if not "aws_access_key_id" in kwargs else kwargs["aws_access_key_id"]
        kwargs["aws_secret_access_key"] = scrts["aws_secret_access_key"] if not "aws_secret_access_key" in kwargs else kwargs["aws_secret_access_key"]
        return self.get_instance(f, service_name, instance_name, [], kwargs)


    def storage_client(self, **kwargs):
        service_name = "storage_client"
        return self._storage_driver(boto3.Session().client, service_name, kwargs)


    def storage_resource(self, **kwargs):
        service_name = "storage_resource"
        return self._storage_driver(boto3.resource, service_name, kwargs)

    def aiostorage_resource(self, **kwargs):
        service_name = "aiostorage_resource"
        return self._storage_driver(aioboto3.Session().resource, service_name, kwargs)

    def aiostorage_client(self, **kwargs):
        service_name = "aiostorage_client"
        return self._storage_driver(aioboto3.Session().client, service_name, kwargs)

    def redis_client(self, **kwargs):
        service_name = "redis_client"
        instance_name = self.def_instance_name if not self.key_istance_name in kwargs else kwargs[self.key_istance_name]
        scrts = self.secrets["redis"]
        cnfg = self.config["redis"]
        kwargs["host"] = cnfg["url"] if not "url" in kwargs else kwargs["url"]
        kwargs["password"] = scrts["password"] if not "password" in kwargs else kwargs["password"]
        kwargs["port"] = cnfg["port"] if not "port" in kwargs else kwargs["port"]
        kwargs["db"] = cnfg["db"] if not "db" in kwargs else kwargs["db"]
        return self.get_instance(redis.Redis, service_name, instance_name, [], kwargs)

    def aioredis_client(self, **kwargs):
        service_name = "aioredis_client"
        instance_name = self.def_instance_name if not self.key_istance_name in kwargs else kwargs[self.key_istance_name]
        scrts = self.secrets["redis"]
        cnfg = self.config["redis"]
        kwargs["host"] = cnfg["url"] if not "url" in kwargs else kwargs["url"]
        kwargs["password"] = scrts["password"] if not "password" in kwargs else kwargs["password"]
        kwargs["port"] = cnfg["port"] if not "port" in kwargs else kwargs["port"]
        kwargs["db"] = cnfg["db"] if not "db" in kwargs else kwargs["db"]
        return self.get_instance(aioredis.Redis, service_name, instance_name, [], kwargs)

