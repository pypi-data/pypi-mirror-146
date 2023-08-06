from typing import List
from avaandmed.api_resources.entities import FileColumn, Preview, SearchResult
from avaandmed.api_resources.datasets.dataset_repository import DatasetRepository
from avaandmed.api_resources.datasets.dataset import Dataset

from avaandmed.exceptions import AvaandmedException
from avaandmed.http.http_client import HttpClient


class Datasets:
    """
    Collection class responsible for actions with Datasets.
    """

    def __init__(self, http_client: HttpClient) -> None:
        self._ENDPOINT = '/datasets'
        self._repository = DatasetRepository(http_client=http_client)

    def get_by_id(self, id: str) -> Dataset:
        """
        Returns Dataset instance with specified id.
        """
        url = f"{self._ENDPOINT}/{id}"
        return self._repository._get_dataset(url)

    def get_by_slug(self, slug: str) -> Dataset:
        """
        Returns Dataset instance with specified slug.
        """
        url = f"{self._ENDPOINT}/slug/{slug}"
        return self._repository._get_dataset(url)

    def get_dataset_list(self, limit: int = 20) -> List[Dataset]:
        """
        Retrieves list of datasets from /datasets endpoint.
        By default returns 20 instances, but limit can be adjusted.
        """
        if limit <= 0:
            raise AvaandmedException('Limit cannot 0 or less.')

        url = f"{self._ENDPOINT}?limit={limit}"
        return self._repository._get_dataset_list(url)

    def get_total(self) -> int:
        """
        Returns total amount of datasets present at the moment.
        """
        url = f"{self._ENDPOINT}/total"
        return self._repository._get_total(url)

    def get_distinct_mimetypes(self) -> List[str]:
        """
        Returns distinct mimetypes used by API.
        """
        url = f"{self._ENDPOINT}/mimetypes/distinct"
        return self._repository._get_distinct_mimetypes(url)

    def get_file_rows_preview(self, id: str, fileId: str) -> Preview:
        """
        Preview the file rows in the way, how end user will see them.
        Returns object according to the provided data in the dataset's file.
        """
        url = f"{self._ENDPOINT}/{id}/files/{fileId}/preview"
        return self._repository._get_file_rows_preview(url)

    def paginate_file_by_id(self, id: str, fileId: str) -> Preview:
        """
        Paginate through successfully processed file content.
        """
        url = f"{self._ENDPOINT}/{id}/files/{fileId}"
        return self._repository._paginate_file_by_id(url)

    def get_file_columns(self, id: str, fileId: str) -> List[FileColumn]:
        """
        Returns columns from the dataset file.
        """
        url = f"{self._ENDPOINT}/{id}/files/{fileId}/columns"
        return self._repository._get_file_columns(url)

    def download_file(self, id: str, fileId: str, out_file: str) -> int:
        """
        Downloads processed file of a dataset.
        By default file will be downloaded into current user's working directory.
        """
        if len(out_file) == 0:
            raise AvaandmedException('File name cannot be empty')

        url = f"{self._ENDPOINT}/{id}/files/{fileId}/download"
        return self._repository._download_file(url, out_file)

    def file_privacy_violations(self, id: str, description: str) -> str:
        """
        Submits privacy violations form for the dataset.
        Returns 'Submitted' status if succesful.
        """
        if len(description) < 20 or len(description) > 1000:
            raise AvaandmedException(
                'Description must be at least 20 characters long, but no longer than 1000.'
            )
        url = f"{self._ENDPOINT}/privacy-violations"
        data = {
            "datasetId": id,
            "description": description
        }
        self._repository._file_privacy_violations(url, data)
        return 'Submitted'

    def apply_for_access(self, id: str, description: str):
        """
        Submits request to get additional permissions for dataset.
        Returns 'Submitted' status if succesful.
        """
        if len(description) < 20 or len(description) > 1000:
            raise AvaandmedException(
                'Description must be at least 20 characters long, but no longer than 1000.'
            )
        url = f"{self._ENDPOINT}/access-permissions"
        data = {
            "datasetId": id,
            "description": description
        }
        self._repository._apply_for_access(url, data)
        return 'Submitted'

    def rate_dataset(self, id: str, quality_rating: int, meta_data_rating: int) -> str:
        """
        Submits rating for the dataset.
        Returns 'Submitted' status if succesful.
        """
        if ((quality_rating < 0 or quality_rating > 10) or
                (meta_data_rating < 0 or meta_data_rating > 10)):
            raise AvaandmedException('Rating must be from 0 to 10.')

        url = f"{self._ENDPOINT}/rating"
        data = {
            "datasetId": id,
            "qualityRating": quality_rating,
            "metadataRating": meta_data_rating
        }
        self._repository._rate_dataset(url, data)
        return 'Submitted'

    def get_dataset_rating_by_slug(self, slug: str) -> str:
        """
        Retrieves rating of the dataset by given slug.
        """
        url = f"{self._ENDPOINT}/rating/{slug}"
        return self._repository._get_dataset_rating_by_slug(url)

    def search(self, keywordId: int, regionId: int, year: int) -> List[SearchResult]:
        """
        Search datasets based on keyword ID, region ID and year.
        Quite limited search capabilities.
        """
        url = f"{self._ENDPOINT}/search?keywordIds={keywordId}&regionIds={regionId}&year={year}"
        return self._repository._search(url)
