from typing import List

from python_http_client.exceptions import HTTPError

from client.v2.fiddler.utils.response_handler import ErrorResponseHandler


class BaseException(Exception):
    pass


class FiddlerException(BaseException):
    # @TODO: Handle standard API error response.
    # How to surface error messages coming form the server. Server responds error messages in a list. Which error to surface?
    def __init__(
        self, status_code: int, error_code: int, message: str, errors: List[str]
    ) -> None:
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        self.errors = errors
        super().__init__(self.message)


def raise_response_error(error: HTTPError) -> FiddlerException:
    error_response = ErrorResponseHandler(error).get_error_details()
    raise FiddlerException(
        error_response.status_code,
        error_response.error_code,
        error_response.message,
        error_response.errors,
    )
