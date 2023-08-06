"""RestService access operations"""
import logging
from typing import Any

from trustedtwin.http_client import HTTPClient
from trustedtwin.operations.docs import DocsOperations
from trustedtwin.operations.identities import IdentitiesOperations
from trustedtwin.operations.ledgers import LedgersOperations
from trustedtwin.operations.roles import RolesOperations
from trustedtwin.operations.secrets import SecretsOperations
from trustedtwin.operations.timeseries import TimeseriesOperations
from trustedtwin.operations.twins import TwinsOperations
from trustedtwin.operations.users import UsersOperations

logger = logging.getLogger('trusted_twin')


DEFAULT_TT_API_HOST = 'https://rest.trustedtwin.com'


class RestService:
    """Represents client accessing API"""

    def __init__(
            self,
            auth: str,
            api_host: str = DEFAULT_TT_API_HOST,
            **kwargs: Any
    ):
        """Initialize object

        :param api_host: url to api host
        :param auth: Authorization secret
        """
        self.http_client = HTTPClient(auth, api_host)
        self.kwargs = kwargs

    @property
    def twins(self) -> TwinsOperations:
        """Return Twins related API operations"""
        return TwinsOperations(self)

    @property
    def ledgers(self) -> LedgersOperations:
        """Return Ledgers related API operations"""
        return LedgersOperations(self)

    @property
    def users(self) -> UsersOperations:
        """Return User related API operations"""
        return UsersOperations(self)

    @property
    def roles(self) -> RolesOperations:
        """Return User related API operations"""
        return RolesOperations(self)

    @property
    def secrets(self) -> SecretsOperations:
        """Return Secret related API operations"""
        return SecretsOperations(self)

    @property
    def identities(self) -> IdentitiesOperations:
        """Return Identities related API operations"""
        return IdentitiesOperations(self)

    @property
    def docs(self) -> DocsOperations:
        """Return Docs related API operations"""
        return DocsOperations(self)

    @property
    def timeseries(self) -> TimeseriesOperations:
        """Return Timeseries related API operations"""
        return TimeseriesOperations(self)
