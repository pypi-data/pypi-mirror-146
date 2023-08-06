import logging
from http import HTTPStatus
from typing import List, Optional

from pydantic import parse_obj_as
from python_http_client.exceptions import HTTPError

from client.v2.fiddler.schema.model import Model
from client.v2.fiddler.utils.exceptions import raise_response_error
from client.v2.fiddler.utils.response_handler import (
    APIResponseHandler,
    PaginatedResponseHandler,
)

logger = logging.getLogger(__name__)


class ModelMixin:
    def get_models(self, project_name: str) -> List[Model]:
        try:
            response = self.client.models.get(
                query_params={
                    'organization_name': self.organization_name,
                    'project_name': project_name,
                }
            )
        except HTTPError as error:
            logger.exception('Failed to get_models')
            raise_response_error(error)
        _, items = PaginatedResponseHandler(response).get_pagination_details_and_items()
        return parse_obj_as(List[Model], items)

    def get_model(self, project_name: str, model_name: str) -> Model:
        try:
            response = self.client.models._(
                f'{self.organization_name}:{project_name}:{model_name}'
            ).get()
        except HTTPError as error:
            logger.exception(f'Failed to get model {model_name}')
            raise_response_error(error)
        response_handler = APIResponseHandler(response)
        return Model.deserialize(response_handler)

    def add_model(
        self,
        project_name: str,
        model_name: str,
        info: Optional[dict] = None,
        model_type: Optional[str] = None,
        framework: Optional[str] = None,
        requirements: Optional[str] = None,
    ) -> Model:
        # @TODO: file_list required while setting up model?
        # @TODO: Handle model_deployment_id?
        try:
            request_body = Model(
                name=model_name,
                info=info,
                model_type=model_type,
                framework=framework,
                requirements=requirements,
            ).dict()
            response = self.client.models._(
                f'{self.organization_name}:{project_name}:{model_name}'
            ).post(request_body=request_body)
        except HTTPError as error:
            logger.exception(f'Failed to setup model {model_name}')
            raise_response_error(error)
        logger.info(f'{model_name} setup successful')
        return Model.deserialize(APIResponseHandler(response))

    def delete_model(self, project_name: str, model_name: str) -> None:
        try:
            response = self.client.models._(
                f'{self.organization_name}:{project_name}:{model_name}'
            ).delete()
        except HTTPError as error:
            logger.exception(f'Failed to delete model {model_name}')
            raise_response_error(error)
        if response.status_code == HTTPStatus.OK:
            logger.info(f'{model_name} delete request received.')
        else:
            # @TODO: Handle non 200 status response
            logger.info('Delete unsuccessful')
