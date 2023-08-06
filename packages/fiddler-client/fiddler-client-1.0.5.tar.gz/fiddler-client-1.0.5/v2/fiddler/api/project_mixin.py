import logging
from http import HTTPStatus
from typing import List

from pydantic import parse_obj_as
from python_http_client.exceptions import HTTPError

from client.v2.fiddler.schema.project import Project
from client.v2.fiddler.utils.exceptions import raise_response_error
from client.v2.fiddler.utils.response_handler import (
    APIResponseHandler,
    PaginatedResponseHandler,
)

logger = logging.getLogger(__name__)


class ProjectMixin:
    def get_projects(self) -> List[Project]:
        try:
            response = self.client.projects.get(
                query_params={'organization_name': self.organization_name}
            )
        except HTTPError as error:
            logger.exception('Failed to get projects')
            raise_response_error(error)
        _, items = PaginatedResponseHandler(response).get_pagination_details_and_items()
        return parse_obj_as(List[Project], items)

    def delete_project(self, project_name: str) -> None:
        try:
            response = self.client.projects._(
                f'{self.organization_name}:{project_name}'
            ).delete()
        except HTTPError as error:
            logger.exception(f'Failed to delete project {project_name}')
            raise_response_error(error)
        if response.status_code == HTTPStatus.OK:
            logger.info(f'{project_name} delete request received.')
        else:
            # @TODO: Handle non 200 status response
            logger.info('Delete unsuccessful')

    def add_project(self, project_name: str) -> Project:
        try:
            request_body = Project(
                name=project_name, organization_name=self.organization_name
            ).dict()
            response = self.client.projects.post(
                query_params={'organization_name': self.organization_name},
                request_body=request_body,
            )
        except HTTPError as error:
            logger.exception(f'Failed to add project {project_name}')
            raise_response_error(error)
        logger.info(f'{project_name} created successfully!')
        return Project.deserialize(APIResponseHandler(response))
