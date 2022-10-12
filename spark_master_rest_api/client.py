import json
from dataclasses import dataclass
from typing import *

from urllib3 import HTTPResponse
from urllib3.connectionpool import HTTPSConnectionPool, HTTPConnectionPool


@dataclass
class SubmitData:
    action: str
    message: str
    server_spark_version: str
    submission_id: str
    success: bool

    @classmethod
    def from_dict(cls, **kwargs):
        return cls(action=kwargs.get('action'),
                   message=kwargs.get('message'),
                   server_spark_version=kwargs.get('serverSparkVersion'),
                   submission_id=kwargs.get('submissionId'),
                   success=kwargs.get('success'))


@dataclass
class StatusData:
    action: str
    driver_state: str
    server_spark_version: str
    submission_id: str
    success: bool
    worker_host_port: str
    worker_id: str

    @classmethod
    def from_dict(cls, **kwargs):
        return cls(action=kwargs.get('action'),
                   driver_state=kwargs.get('driverState'),
                   server_spark_version=kwargs.get('serverSparkVersion'),
                   submission_id=kwargs.get('submissionId'),
                   success=kwargs.get('success'),
                   worker_host_port=kwargs.get('workerHostPort'),
                   worker_id=kwargs.get('workerId'))


@dataclass
class KillData:
    action: str
    message: str
    server_spark_version: str
    submission_id: str
    success: bool

    @classmethod
    def from_dict(cls, **kwargs):
        return cls(action=kwargs.get('action'),
                   message=kwargs.get('message'),
                   server_spark_version=kwargs.get('serverSparkVersion'),
                   submission_id=kwargs.get('submissionId'),
                   success=kwargs.get('success'))


class Client:
    def __init__(self,
                 host: str,
                 spark_version: str,
                 port: int = 6066,
                 maxsize: int = 1,
                 secure: bool = False,
                 **kwargs):
        _forbidden_keys = {'host', 'port', 'maxsize', 'secure'}
        _ = {kwargs.pop(_key, None) for _key in _forbidden_keys}
        if secure:
            self._connection_pool = HTTPSConnectionPool(host=host,
                                                        port=port,
                                                        maxsize=maxsize)
        else:
            self._connection_pool = HTTPConnectionPool(host=host,
                                                       port=port,
                                                       maxsize=maxsize)
        self.spark_version = spark_version

    def submit(
            self,
            app_resource: str,
            spark_properties: dict,
            main_class: str = 'org.apache.spark.deploy.SparkSubmit',
            environment_variables: dict = None,
            app_args: list = None
    ):
        _response = self._connection_pool.request('POST',
                                                  url='/v1/submissions/create',
                                                  headers={
                                                      'Content-Type': 'application/json;charset=UTF-8',
                                                  },
                                                  body=json.dumps({
                                                      'appResource': app_resource,
                                                      'sparkProperties': spark_properties,
                                                      'clientSparkVersion': self.spark_version,
                                                      'mainClass': main_class,
                                                      'environmentVariables': environment_variables or dict(),
                                                      'action': 'CreateSubmissionRequest',
                                                      'appArgs': app_args or list(),
                                                  }))
        return _response, self._to_model(_response, SubmitData)

    def status(self, driver_id: str):
        driver_id = driver_id.split('/')[0]
        path = f'/v1/submissions/status/{driver_id}'
        _response = self._connection_pool.request('GET',
                                                  url=path,
                                                  headers={
                                                      'Content-Type': 'application/json;charset=UTF-8',
                                                  })
        return _response, self._to_model(_response, StatusData)

    def kill(self, driver_id: str):
        driver_id = driver_id.split('/')[0]
        path = f'/v1/submissions/kill/{driver_id}'
        _response = self._connection_pool.request('POST',
                                                  url=path,
                                                  headers={
                                                      'Content-Type': 'application/json;charset=UTF-8',
                                                  })
        return _response, self._to_model(_response, KillData)

    @staticmethod
    def _is_successful(_response):
        return 200 <= _response.status < 300

    @classmethod
    def _to_model(cls,
                  response: HTTPResponse,
                  model: Union[Type[KillData], Type[StatusData], Type[SubmitData]],
                  encoding='utf-8'):
        if cls._is_successful(response):
            _json_response = json.loads(response.data.decode(encoding))
            return model.from_dict(**_json_response)
        return None
