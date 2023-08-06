"""Definition of Ledgers resources methods"""
from enum import Enum
from typing import TYPE_CHECKING, Dict, List, Union, Optional, Any
from uuid import UUID

from trustedtwin.misc import RESTMethod
from trustedtwin.models.responses import process_response

if TYPE_CHECKING:
    from trustedtwin.service import RestService


class TTLedgerAlias(str, Enum):
    """Possible resource aliases."""
    PERSONAL = 'personal'
    OWNER = 'owner'
    CREATOR = 'creator'


class LedgersOperations:
    """Interface for accessing Ledgers operations"""

    def __init__(self, service: 'RestService'):
        """Initialize object"""
        self._service = service
        self._http_client = self._service.http_client
        self._endpoint_base = 'twins/{twin}/ledgers'

    def add_twin_ledger_entry(
            self,
            twin: str,
            entries: Dict,
            ledger: Union[UUID, TTLedgerAlias] = TTLedgerAlias.PERSONAL,
            **kwargs: Any
    ) -> Dict:
        """Execute addTwinLedgerEntry API operation"""

        endpoint = self._endpoint_base.format(twin=twin)
        endpoint = '{}/{}'.format(endpoint, ledger)

        payload = {
            'entries': entries
        }

        resp = self._http_client.execute_request(
            method=RESTMethod.POST,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            body=payload,
            **kwargs
        )

        return process_response(resp, 'addTwinLedgerEntry', **self._service.kwargs)

    def get_twin_ledger_entry(
            self,
            twin: str,
            ledger: Union[str, TTLedgerAlias] = TTLedgerAlias.PERSONAL,
            entries: Optional[List[str]] = None,
            show_references: bool = True,
            show_public: bool = True,
            show_private: bool = True,
            **kwargs: Any
    ) -> Dict:
        """Execute getTwinLedgerEntry API operation"""
        endpoint = self._endpoint_base.format(twin=twin)
        endpoint = '{}/{}'.format(endpoint, ledger)

        params = {
            'show_references': show_references,
            'show_public': show_public,
            'show_private': show_private
        }
        if entries:
            params['entries'] = ','.join(entries)

        resp = self._http_client.execute_request(
            method=RESTMethod.GET,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            params=params,
            **kwargs
        )

        return process_response(resp, 'getTwinLedgerEntry', **self._service.kwargs)

    def delete_twin_ledger_entry(
            self,
            twin: str,
            ledger: Union[str, TTLedgerAlias] = TTLedgerAlias.PERSONAL,
            entries: Optional[List[str]] = None
    ) -> Dict:
        """Execute deleteTwinLedgerEntry API operation"""
        endpoint = self._endpoint_base.format(twin=twin)
        endpoint = '{}/{}'.format(endpoint, ledger)

        params = {}
        if entries:
            params['entries'] = ','.join(entries)

        resp = self._http_client.execute_request(
            method=RESTMethod.DELETE,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            params=params
        )

        return process_response(resp, 'deleteTwinLedgerEntry', **self._service.kwargs)

    def update_twin_ledger_entry(
            self,
            twin: str,
            entries: Dict,
            ledger: Union[str, TTLedgerAlias] = TTLedgerAlias.PERSONAL,
            **kwargs: Any
    ) -> Dict:
        """Execute updateTwinLedgerEntry API operation"""
        endpoint = self._endpoint_base.format(twin=twin)
        endpoint = '{}/{}'.format(endpoint, ledger)
        payload = {
            'entries': entries
        }

        resp = self._http_client.execute_request(
            method=RESTMethod.PATCH,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            body=payload,
            **kwargs
        )

        return process_response(resp, 'updateTwinLedgerEntry', **self._service.kwargs)
