import logging
from http import HTTPStatus
from typing import List

from pydantic import parse_obj_as
from python_http_client.exceptions import HTTPError

from client.v2.fiddler.schema.dataset import Dataset
from client.v2.fiddler.utils.exceptions import raise_response_error
from client.v2.fiddler.utils.response_handler import (
    APIResponseHandler,
    PaginatedResponseHandler,
)

logger = logging.getLogger(__name__)


class DatasetMixin:
    def get_datasets(self, project_name: str) -> List[Dataset]:
        try:
            response = self.client.datasets.get(
                query_params={
                    'organization_name': self.organization_name,
                    'project_name': project_name,
                }
            )
        except HTTPError as error:
            logger.exception(f'Failed to get datasets for project: {project_name}')
            raise_response_error(error)
        _, items = PaginatedResponseHandler(response).get_pagination_details_and_items()
        return parse_obj_as(List[Dataset], items)

    def get_dataset(self, project_name: str, dataset_name: str) -> Dataset:
        try:
            response = self.client.datasets._(
                f'{self.organization_name}:{project_name}:{dataset_name}'
            ).get()
        except HTTPError as error:
            logger.exception(f'Failed to get dataset {dataset_name}')
            raise_response_error(error)
        response_handler = APIResponseHandler(response)
        return Dataset.deserialize(response_handler)

    def delete_dataset(self, project_name: str, dataset_name: str) -> None:
        try:
            response = self.client.datasets._(
                f'{self.organization_name}:{project_name}:{dataset_name}'
            ).delete()
        except HTTPError as error:
            logger.exception(f'Failed to delete datasets: {dataset_name}')
            raise_response_error(error)
        if response.status_code == HTTPStatus.OK:
            logger.info(f'{dataset_name} delete request received.')
        else:
            # @TODO: Handle non 200 status response
            logger.info('Delete unsuccessful')
