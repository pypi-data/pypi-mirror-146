"""Definition of Roles resources methods"""
from typing import TYPE_CHECKING, Dict
from uuid import UUID

from trustedtwin.misc import RESTMethod
from trustedtwin.models.responses import process_response

if TYPE_CHECKING:
    from trustedtwin.service import RestService


class RolesOperations:
    """Interface for accessing Roles API operations"""

    def __init__(self, service: 'RestService'):
        """Initialize object"""
        self._service = service
        self._http_client = self._service.http_client
        self._endpoint_base = 'roles'

    def create(self, payload: Dict) -> Dict:
        """Execute createUserRole API operation"""
        resp = self._http_client.execute_request(
            method=RESTMethod.POST,
            url_root=self._http_client.host_name,
            endpoint=self._endpoint_base,
            body=payload
        )

        return process_response(resp, 'createUserRole', **self._service.kwargs)

    def get(self, role_uuid: UUID) -> Dict:
        """Execute getUserRole API operation"""
        endpoint = '{}/{}'.format(self._endpoint_base, str(role_uuid))

        resp = self._http_client.execute_request(
            method=RESTMethod.GET,
            url_root=self._http_client.host_name,
            endpoint=endpoint
        )

        return process_response(resp, 'getUserRole', **self._service.kwargs)

    def get_all(self) -> Dict:
        """Execute getUserRoles API operation"""
        endpoint = self._endpoint_base

        resp = self._http_client.execute_request(
            method=RESTMethod.GET,
            url_root=self._http_client.host_name,
            endpoint=endpoint
        )

        return process_response(resp, 'getUserRoles', **self._service.kwargs)

    def update(self, role_uuid: UUID, payload: Dict) -> Dict:
        """Execute updateUserRole API operation"""
        endpoint = '{}/{}'.format(self._endpoint_base, str(role_uuid))

        resp = self._http_client.execute_request(
            method=RESTMethod.PATCH,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            body=payload
        )

        return process_response(resp, 'updateUserRole', **self._service.kwargs)

    def delete(self, role_uuid: UUID) -> Dict:
        """Execute deleteUserRole API operation"""
        endpoint = '{}/{}'.format(self._endpoint_base, str(role_uuid))

        resp = self._http_client.execute_request(
            method=RESTMethod.DELETE,
            url_root=self._http_client.host_name,
            endpoint=endpoint
        )

        return process_response(resp, 'deleteUserRole', **self._service.kwargs)
