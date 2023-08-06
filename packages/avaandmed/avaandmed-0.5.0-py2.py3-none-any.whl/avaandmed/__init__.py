from typing import Optional, List

from pydantic import parse_obj_as
from avaandmed.api_resources.entities import (
    Category,
    CoordinateReferenceSystem,
    EmsCategory,
    KeywordInfo,
    Language,
    Licence,
    Region)
from avaandmed.api_resources.organizations import Organizations
from avaandmed.http.http_client import HttpClient, HttpMethod


class Avaandmed:
    """A client for accessing Avaadnmed API"""

    def __init__(self, api_token: str, key_id: str, base_hostname: str = 'avaandmed.eesti.ee') -> None:
        self._api_token = api_token
        self._key_id = key_id
        self._http_client = HttpClient(base_hostname, api_token, key_id)
        self._datasets = None
        self._organizations = None  # type: Optional[Organizations]
        self._users = None

    @property
    def api_token(self) -> str:
        return self._api_token

    @property
    def key_id(self) -> str:
        return self._key_id

    @property
    def datasets(self):
        if self._datasets is None:
            from avaandmed.api_resources.datasets import Datasets
            self._datasets = Datasets(http_client=self._http_client)
        return self._datasets

    def organizations(self, id: str):
        if self._organizations is None:
            from avaandmed.api_resources.organizations import Organizations
            self._organizations = Organizations(
                id=id, http_client=self._http_client)
        return self._organizations

    @property
    def users(self):
        if self._users is None:
            from avaandmed.api_resources.users import Users
            self._users = Users(http_client=self._http_client)
        return self._users

    def get_categories(self) -> List[Category]:
        response = self.__get('/categories')
        return parse_obj_as(List[Category], response)

    def get_euro_categories(self) -> List[Category]:
        response = self.__get('/euro-categories')
        return parse_obj_as(List[Category], response)

    def get_ems_categories(self) -> List[EmsCategory]:
        response = self.__get('/ems-categories')
        return parse_obj_as(List[EmsCategory], response)

    def get_regions(self) -> List[Region]:
        response = self.__get('/regions')
        return parse_obj_as(List[Region], response)

    def get_coordinate_ref_system(self) -> List[CoordinateReferenceSystem]:
        response = self.__get('/coordinateReferenceSystems')
        return parse_obj_as(List[CoordinateReferenceSystem], response)

    def get_languages(self) -> List[Language]:
        response = self.__get('/languages')
        return parse_obj_as(List[Language], response)

    def get_keywords(self, search_word: str = '', limit=20):
        """
        Retrieves first 20 keywords by defualt.
        You can also provide some specific search word to limit or extend 
        scope of keywords you are looking for.
        """
        response = self.__get(f"/keywords?search={search_word}&limit={limit}")
        return parse_obj_as(List[KeywordInfo], response)

    def get_licenses(self) -> List[Licence]:
        response = self.__get('/licences')
        return parse_obj_as(List[Licence], response)

    def __get(self, url: str):
        return self._http_client.request(HttpMethod.GET, url)
