"""Definition of Docs resources methods"""
import urllib.parse
from typing import TYPE_CHECKING, Dict, Optional

from trustedtwin.misc import RESTMethod
from trustedtwin.models.responses import process_response

if TYPE_CHECKING:
    from trustedtwin.service import RestService


class DocsOperations:
    """Interfaces for accessing Docs API operations"""

    def __init__(self, service: 'RestService'):
        """Initialize object"""
        self._service = service
        self._http_client = self._service.http_client
        self._endpoint_base = 'twins/{twin}/docs'

    def create_upload_url(self) -> Dict:
        """Execute createUploadURL API operation"""
        endpoint = 'cache'

        resp = self._http_client.execute_request(
            method=RESTMethod.POST,
            url_root=self._http_client.host_name,
            endpoint=endpoint
        )

        return process_response(resp, 'createUploadURL', **self._service.kwargs)

    def attach_twin_doc(self, twin: str, docs: Dict) -> Dict:
        """Execute attachTwinDoc API operation"""
        endpoint = self._endpoint_base.format(twin=twin)

        payload = {
            'docs': docs
        }

        resp = self._http_client.execute_request(
            method=RESTMethod.POST,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            body=payload
        )

        return process_response(resp, 'attachTwinDoc', **self._service.kwargs)

    def get_twin_doc(self, twin: str, doc_name: str, download: bool = False) -> Dict:
        """Execute getTwinDoc API operation"""
        endpoint = '{}/{}'.format(
            self._endpoint_base.format(twin=twin),
            urllib.parse.quote(doc_name, safe='')
        )

        query_params = {
            'download': download
        }

        resp = self._http_client.execute_request(
            method=RESTMethod.GET,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            params=query_params
        )

        return process_response(resp, 'getTwinDoc', **self._service.kwargs)

    def get_twin_docs(self, twin: str, view: Optional[str] = None) -> Dict:
        """Execute getTwinDocs API operation"""
        params = {}
        if view:
            params['view'] = view

        resp = self._http_client.execute_request(
            method=RESTMethod.GET,
            url_root=self._http_client.host_name,
            endpoint=self._endpoint_base.format(twin=twin),
            params=params
        )

        return process_response(resp, 'getTwinDocs', **self._service.kwargs)

    def invalidate_upload_url(self, handler: str) -> Dict:
        """Execute invalidateUploadURL"""
        endpoint = 'cache/{}'.format(handler)

        resp = self._http_client.execute_request(
            method=RESTMethod.DELETE,
            url_root=self._http_client.host_name,
            endpoint=endpoint
        )

        return process_response(resp, 'invalidateUploadURL', **self._service.kwargs)

    def update_twin_doc(self, twin: str, doc_name: str, description: Optional[Dict] = None) -> Dict:
        """Execute updateTwinDoc API operation"""
        endpoint = '{}/{}'.format(self._endpoint_base.format(twin=twin), doc_name)
        payload = {
            'description': description
        }

        resp = self._http_client.execute_request(
            method=RESTMethod.PATCH,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            body=payload
        )

        return process_response(resp, 'updateTwinDoc', **self._service.kwargs)

    def delete_twin_doc(self, twin: str, doc_name: str) -> Dict:
        """Execute deleteTwinDoc API operation"""
        endpoint = '{}/{}'.format(
            self._endpoint_base.format(twin=twin),
            urllib.parse.quote(doc_name, safe='')
        )

        resp = self._http_client.execute_request(
            method=RESTMethod.DELETE,
            url_root=self._http_client.host_name,
            endpoint=endpoint
        )

        return process_response(resp, 'deleteTwinDoc', **self._service.kwargs)

    def delete_twin_docs(self, twin: str) -> Dict:
        """Execute deleteTwinDocs API operation"""
        endpoint = self._endpoint_base.format(twin=twin)

        resp = self._http_client.execute_request(
            method=RESTMethod.DELETE,
            url_root=self._http_client.host_name,
            endpoint=endpoint
        )

        return process_response(resp, 'deleteTwinDocs', **self._service.kwargs)
