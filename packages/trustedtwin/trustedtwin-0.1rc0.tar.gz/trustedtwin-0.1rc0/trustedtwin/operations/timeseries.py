"""Definition of Timeseries operations access methods"""
from typing import TYPE_CHECKING, Dict

from trustedtwin.misc import RESTMethod

if TYPE_CHECKING:
    from trustedtwin.service import RestService


class TimeseriesOperations:
    """Interface for accessing Timeseries API operations"""

    def __init__(self, service: 'RestService'):
        """Initialize object"""
        self._service = service
        self._http_client = self._service.http_client
        self._endpoint_base = 'account/services/timeseries'

    def create_timeseries_table(self, timeseries: Dict) -> Dict:
        """Execute createTimeseriesTable API operation"""

        payload = {
            'timeseries': timeseries
        }

        return self._http_client.execute_request(
            method=RESTMethod.POST,
            url_root=self._http_client.api_host,
            endpoint=self._endpoint_base,
            body=payload
        )

    def delete_timeseries_table(self, table: str) -> Dict:
        """Execute deleteTimeseriesTable API operation"""

        return self._http_client.execute_request(
            method=RESTMethod.DELETE,
            url_root=self._http_client.api_host,
            endpoint="{}/{}".format(self._endpoint_base, table),
        )

    def get_timeseries_table(self, table: str) -> Dict:
        """Execute getTimeseriesTable API operation"""

        return self._http_client.execute_request(
            method='GET',
            url_root=self._http_client.api_host,
            endpoint="{}/{}".format(self._endpoint_base, table),
        )

    def update_timeseries_table(self, table: str, payload: Dict) -> Dict:
        """Execute updateTimeseriesTable API operation"""

        return self._http_client.execute_request(
            method=RESTMethod.PATCH,
            url_root=self._http_client.api_host,
            endpoint="{}/{}".format(self._endpoint_base, table),
            body=payload
        )

    def truncate_timeseries_table(self, table: str) -> Dict:
        """Execute truncateTimeseriesTable API operation"""

        return self._http_client.execute_request(
            method=RESTMethod.DELETE,
            url_root=self._http_client.api_host,
            endpoint="{}/{}/data".format(self._endpoint_base, table),
        )

    def get_timeseries_tables(self) -> Dict:
        """Execute getTimeseriesTables API operation"""

        return self._http_client.execute_request(
            method=RESTMethod.GET,
            url_root=self._http_client.api_host,
            endpoint=self._endpoint_base,
        )

    def update_timeseries_access(self, users: Dict) -> Dict:
        """Execute updateTimeseriesAccess API operation"""

        payload = {
            'users': users
        }

        return self._http_client.execute_request(
            method=RESTMethod.PATCH,
            url_root=self._http_client.api_host,
            endpoint=self._endpoint_base,
            body=payload
        )
