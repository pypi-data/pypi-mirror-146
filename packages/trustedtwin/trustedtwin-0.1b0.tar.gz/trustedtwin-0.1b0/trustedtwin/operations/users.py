"""Definition of Users resources methods"""
from typing import TYPE_CHECKING, Dict

from trustedtwin.misc import RESTMethod
from trustedtwin.models.responses import process_response

if TYPE_CHECKING:
    from trustedtwin.service import RestService


class UsersOperations:
    """Interface for accessing Users operations"""

    def __init__(self, service: 'RestService'):
        """Initialize object"""
        self._service = service
        self._http_client = self._service.http_client
        self._endpoint_base = 'users'

    def create(self, payload: Dict) -> Dict:
        """Execute createUser API operation"""
        resp = self._http_client.execute_request(
            method=RESTMethod.POST,
            url_root=self._http_client.host_name,
            endpoint=self._endpoint_base,
            body=payload
        )

        return process_response(resp, 'createUser', **self._service.kwargs)

    def get(self, user: str) -> Dict:
        """Execute getUser API operation"""
        endpoint = '{}/{}'.format(self._endpoint_base, str(user))

        resp = self._http_client.execute_request(
            method=RESTMethod.GET,
            url_root=self._http_client.host_name,
            endpoint=endpoint
        )

        return process_response(resp, 'getUser', **self._service.kwargs)

    def update(self, user: str, payload: Dict) -> Dict:
        """Execute updateUser API operation"""
        endpoint = '{}/{}'.format(self._endpoint_base, user)

        resp = self._http_client.execute_request(
            method=RESTMethod.PATCH,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            body=payload
        )

        return process_response(resp, 'updateUser', **self._service.kwargs)

    def delete(self, user: str) -> Dict:
        """Execute deleteUser API operation"""
        endpoint = '{}/{}'.format(self._endpoint_base, user)

        resp = self._http_client.execute_request(
            method=RESTMethod.DELETE,
            url_root=self._http_client.host_name,
            endpoint=endpoint
        )

        return process_response(resp, 'deleteUser', **self._service.kwargs)
