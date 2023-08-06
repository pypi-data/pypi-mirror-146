"""Definition of Identities resources methods"""
import urllib
from enum import Enum
from typing import Dict, TYPE_CHECKING, Optional, Any

from trustedtwin.misc import RESTMethod
from trustedtwin.models.responses import process_response

if TYPE_CHECKING:
    from trustedtwin.service import RestService


class IdentityContextAlias(str, Enum):
    """Possible identity search context (url suffix) """
    PERSONAL = 'personal'
    SYSTEM = 'system'


class IdentitiesOperations:
    """Interfaces for accessing Identities API operations"""

    def __init__(self, service: 'RestService'):
        """Initialize object"""
        self._service = service
        self._http_client = self._service.http_client
        self._endpoint_base = 'twins/{twin}/identities'

    def create(self, twin: str, identities: Dict, **kwargs: Any) -> Dict:
        """Execute createTwinIdentity API operation"""
        endpoint = self._endpoint_base.format(twin=twin)

        payload = {
            'identities': identities
        }

        resp = self._http_client.execute_request(
            method=RESTMethod.POST,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            body=payload,
            **kwargs
        )

        return process_response(resp, 'createTwinIdentity', **self._service.kwargs)

    def update(
            self,
            twin: str,
            identity: str,
            visibility: Optional[str] = None,
            validity_ts: Optional[float] = None
    ) -> Dict:
        """Execute updateTwinIdentity API operation"""
        endpoint = self._endpoint_base.format(twin=twin)
        endpoint = '{}/{}'.format(endpoint, urllib.parse.quote(identity))   # type: ignore

        payload: Dict[str, Any] = {}
        if visibility:
            payload['visibility'] = visibility

        if validity_ts:
            payload['validity_ts'] = validity_ts

        resp = self._http_client.execute_request(
            method=RESTMethod.PATCH,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            body=payload
        )

        return process_response(resp, 'updateTwinIdentity', **self._service.kwargs)

    def delete(self, twin: str, identity: str) -> Dict:
        """Execute deleteTwinIdentity API operation"""
        endpoint = self._endpoint_base.format(twin=twin)
        endpoint = '{}/{}'.format(endpoint, urllib.parse.quote(identity))       # type: ignore

        resp = self._http_client.execute_request(
            method=RESTMethod.DELETE,
            url_root=self._http_client.host_name,
            endpoint=endpoint
        )

        return process_response(resp, 'deleteTwinIdentity', **self._service.kwargs)

    def get(self, twin: str, identity: str) -> Dict:
        """Execute getTwinIdentity API operation"""
        endpoint = self._endpoint_base.format(twin=twin)
        endpoint = '{}/{}'.format(endpoint, urllib.parse.quote(identity))       # type: ignore

        resp = self._http_client.execute_request(
            method=RESTMethod.GET,
            url_root=self._http_client.host_name,
            endpoint=endpoint
        )

        return process_response(resp, 'getTwinIdentity', **self._service.kwargs)

    def get_identities(
            self,
            twin: str,
            show_expired: Optional[bool] = None,
            show_valid: Optional[bool] = None,
            show_foreign: Optional[bool] = None,
            show_personal: Optional[bool] = None,
            show_public: Optional[bool] = None,
            show_private: Optional[bool] = None
    ) -> Dict:
        """Execute getTwinIdentities API operation"""
        endpoint = self._endpoint_base.format(twin=twin)
        params = {
            'show_expired': show_expired,
            'show_valid': show_valid,
            'show_foreign': show_foreign,
            'show_personal': show_personal,
            'show_public': show_public,
            'show_private': show_private
        }
        resp = self._http_client.execute_request(
            method=RESTMethod.GET,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            params=params)

        return process_response(resp, 'getTwinIdentities', **self._service.kwargs)

    def resolve(self, identity: str, context: IdentityContextAlias) -> Dict:
        """Execute resolveIdentity API operation"""
        endpoint = 'resolve/{identity}'.format(identity=urllib.parse.quote(identity))       # type: ignore

        params = {}
        if context is not None:
            params['context'] = context.value

        resp = self._http_client.execute_request(
            method=RESTMethod.GET,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            params=params)

        return process_response(resp, 'resolveIdentity', **self._service.kwargs)
