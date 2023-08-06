"""Definition of Twins resources methods"""
from typing import TYPE_CHECKING, Dict, Optional

from trustedtwin.misc import RESTMethod
from trustedtwin.models.responses import process_response

if TYPE_CHECKING:
    from trustedtwin.service import RestService


class TwinsOperations:
    """Interface for accessing Twins operations"""

    def __init__(self, service: 'RestService'):
        """Initialize object"""
        self._service = service
        self._http_client = self._service.http_client
        self._endpoint_base = 'twins'

    def create(self, description: Optional[Dict] = None) -> Dict:
        """Execute createTwin API operation"""
        endpoint = '{}'.format(self._endpoint_base)

        payload = {}
        if description:
            payload['description'] = description

        resp = self._http_client.execute_request(
            method=RESTMethod.POST,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            body=payload
        )

        return process_response(resp, 'createTwin', **self._service.kwargs)

    def update(self, twin: str, description: Optional[Dict] = None) -> Dict:
        """Execute updateTwin API operation"""
        endpoint = '{}/{}'.format(self._endpoint_base, twin)
        payload = {}
        if description:
            payload['description'] = description

        resp = self._http_client.execute_request(
            method=RESTMethod.PATCH,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            body=payload
        )

        return process_response(resp, 'updateTwin', **self._service.kwargs)

    def get(self, twin: str, show_terminated: Optional[bool] = None) -> Dict:
        """Execute getTwin API operation"""
        endpoint = '{}/{}'.format(self._endpoint_base, twin)

        query_params = {}
        if show_terminated is not None:
            query_params['show_terminated'] = show_terminated

        resp = self._http_client.execute_request(
            method=RESTMethod.GET,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            params=query_params
        )

        return process_response(resp, 'getTwin', **self._service.kwargs)

    def terminate(self, twin: str) -> Dict:
        """Execute terminateTwin API operation"""
        endpoint = '{}/{}'.format(self._endpoint_base, twin)

        resp = self._http_client.execute_request(
            method=RESTMethod.DELETE,
            url_root=self._http_client.host_name,
            endpoint=endpoint
        )

        return process_response(resp, 'terminateTwin', **self._service.kwargs)
