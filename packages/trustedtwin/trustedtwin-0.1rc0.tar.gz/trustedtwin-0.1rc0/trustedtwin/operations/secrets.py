"""Definition of Secrets resources methods"""
from typing import TYPE_CHECKING, Dict, Optional
from uuid import UUID

from trustedtwin.misc import RESTMethod
from trustedtwin.models.responses import process_response

if TYPE_CHECKING:
    from trustedtwin.service import RestService


class SecretsOperations:
    """Interface for accessing Secrets API operations"""

    def __init__(self, service: 'RestService'):
        """Initialize object"""
        self._service = service
        self._http_client = self._service.http_client
        self._endpoint_base = 'secrets'

    def create_secret(self, account: UUID, pin: str) -> Dict:
        """Execute createUserRole API operation"""
        endpoint = '{base}/{account}/{pin}'.format(
            base=self._endpoint_base,
            account=str(account),
            pin=pin
        )

        resp = self._http_client.execute_request(
            method=RESTMethod.POST,
            url_root=self._http_client.host_name,
            endpoint=endpoint
        )

        return process_response(resp, 'createUserRole', **self._service.kwargs)

    def create_secret_pin(self, user: str, validity_ts: Optional[float] = None) -> Dict:
        """Execute createSecretPin API operation"""
        endpoint = 'users/{}/secrets'.format(user)
        payload = {}
        if validity_ts:
            payload['validity_ts'] = validity_ts

        resp = self._http_client.execute_request(
            method=RESTMethod.POST,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            body=payload
        )

        return process_response(resp, 'createSecretPin', **self._service.kwargs)

    def update_secret(self, user: str, validity_ts: float) -> Dict:
        """Execute updateUserSecret API operation"""
        endpoint = 'users/{}/secrets'.format(user)
        payload = {}
        if validity_ts:
            payload['validity_ts'] = validity_ts

        resp = self._http_client.execute_request(
            method=RESTMethod.PATCH,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            body=payload
        )

        return process_response(resp, 'updateUserSecret', **self._service.kwargs)

    def get_secret(self, user: str) -> Dict:
        """Execute getUserSecret API operation"""
        endpoint = 'users/{}/secrets'.format(user)

        resp = self._http_client.execute_request(
            method=RESTMethod.GET,
            url_root=self._http_client.host_name,
            endpoint=endpoint
        )

        return process_response(resp, 'getUserSecret', **self._service.kwargs)

    def delete_secret(self, user: str) -> Dict:
        """Execute deleteUserSecret API operation"""
        endpoint = 'users/{}/secrets'.format(user)

        resp = self._http_client.execute_request(
            method=RESTMethod.DELETE,
            url_root=self._http_client.host_name,
            endpoint=endpoint
        )

        return process_response(resp, 'deleteUserSecret', **self._service.kwargs)
