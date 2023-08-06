from abc import ABC


class AdapterError(Exception):
    pass


class BaseAdapter(ABC):
    _client_error_codes: dict = dict()
    _client_exception_class = None
    _server_exception_class = None

    def __init__(self):
        if None in (self._client_exception_class, self._server_exception_class):
            raise AdapterError('Exception classes not set.')
        super().__init__()

    def _raise_exception(self, error_message: str = None, is_server_error=False):
        if not is_server_error and error_message is None:
            raise AdapterError('Set error message for client error.')
        if is_server_error:
            raise self._server_exception_class('server_error')
        else:
            raise self._client_exception_class(self._get_error_code(error_message=error_message))

    def _get_error_code(self, error_message: str):
        if not isinstance(error_message, str):
            raise AdapterError('Only string error message accepted.')
        for key, value in self._client_error_codes.items():
            if error_message in value:
                return key
        return 'unknown_client_error'


class BaseFactory:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
