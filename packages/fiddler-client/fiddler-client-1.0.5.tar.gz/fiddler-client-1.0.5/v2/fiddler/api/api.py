import logging

from python_http_client import Client as PythonHttpClient

from client.v2.fiddler.api.dataset_mixin import DatasetMixin
from client.v2.fiddler.api.model_mixin import ModelMixin
from client.v2.fiddler.api.project_mixin import ProjectMixin

logger = logging.getLogger(__name__)
URL_PREFIX = '/v2'


class Client(ModelMixin, DatasetMixin, ProjectMixin):
    def __init__(self, url: str, organization_name: str, auth_token: str) -> None:
        self.url = url
        self.auth_token = auth_token
        self.organization_name = organization_name
        self.client = PythonHttpClient(
            host=url + URL_PREFIX,
            request_headers={'Authorization': f'Bearer {auth_token}'},
        )
