import json
import logging
from collections import namedtuple
from typing import List, NamedTuple, Tuple

from python_http_client.client import Response
from python_http_client.exceptions import HTTPError

logger = logging.getLogger(__name__)


class BaseResponseHandler:
    def __init__(self, response: Response) -> None:
        self.response = response

    def get_data(self) -> dict:
        dict_response = json.loads(self.response.body).get('data')
        dict_response.pop('kind', None)
        dict_response.pop('created_by', None)
        dict_response.pop('updated_by', None)
        dict_response.pop('created_at', None)
        dict_response.pop('updated_at', None)
        return dict_response

    def get_status_code(self) -> int:
        return self.response.status_code


class PaginatedResponseHandler(BaseResponseHandler):
    '''
    Handle fiddler OAS's standard Paginated response
    '''

    def get_pagination_details_and_items(self) -> Tuple[dict, List[dict]]:
        data = self.get_data()
        items = data.pop('items')
        return data, items


class APIResponseHandler(BaseResponseHandler):
    '''
    Handle fiddler OAS's standard API Response
    '''


class ErrorResponseHandler:
    def __init__(self, http_error: HTTPError) -> None:
        self.http_error = http_error
        self.ErrorResponse = namedtuple(
            'ErrorResponse', ['status_code', 'error_code', 'message', 'errors']
        )

    def get_error_details(self) -> NamedTuple:
        status_code = self.http_error.status_code
        error_details = self.http_error.to_dict.get('error', {})
        error_code = error_details.get('code')
        message = error_details.get('message')
        errors = error_details.get('errors')
        return self.ErrorResponse(status_code, error_code, message, errors)
