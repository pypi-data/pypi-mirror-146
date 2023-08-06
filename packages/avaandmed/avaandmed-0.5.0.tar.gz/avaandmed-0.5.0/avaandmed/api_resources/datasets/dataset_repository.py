from typing import List
from pydantic import parse_obj_as
from avaandmed.http.http_client import HttpClient, HttpMethod
from avaandmed.api_resources.datasets.dataset import Dataset
from avaandmed.api_resources.entities import (
    AccessPermission,
    DatasetMetadata,
    DatasetRatingList,
    File,
    FileColumn,
    FileErrors,
    Index,
    Preview,
    PrivacyViolation,
    SearchResult
)


class DatasetRepository:

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client

    def _get_dataset(self, url: str) -> Dataset:
        dataset_json = self._http_client.request(HttpMethod.GET, url=url)
        return Dataset.parse_obj(dataset_json)

    def _get_dataset_list(self, url: str) -> List[Dataset]:
        datasets_json = self._http_client.request(HttpMethod.GET, url=url)
        dataset_list = parse_obj_as(List[Dataset], datasets_json)
        return dataset_list

    def _get_total(self, url: str) -> int:
        total = self._http_client.request(HttpMethod.GET, url=url)
        return total

    def _get_distinct_mimetypes(self, url: str) -> List[str]:
        mimetypes = self._http_client.request(HttpMethod.GET, url=url)
        return mimetypes

    def _get_file_rows_preview(self, url: str) -> Preview:
        preview = self._http_client.request(HttpMethod.GET, url=url)
        return preview

    def _paginate_file_by_id(self, url: str) -> Preview:
        file = self._http_client.request(HttpMethod.GET, url=url)
        return file

    def _get_file_columns(self, url: str) -> List[FileColumn]:
        columns = self._http_client.request(HttpMethod.GET, url=url)
        return parse_obj_as(List[FileColumn], columns)

    def _download_file(self, url: str, out_file: str, json={}) -> int:
        return self._http_client.download(url, out_file, json)

    def _file_privacy_violations(self, url: str, data: dict) -> str:
        body = {
            "datasetId": data['datasetId'],
            "description": data['description']
        }
        self._http_client.request(HttpMethod.POST, url, body)
        return 'Submitted'

    def _apply_for_access(self, url: str, data: dict):
        body = {
            "datasetId": data['datasetId'],
            "description": data['description']
        }
        self._http_client.request(HttpMethod.POST, url, body)
        return 'Submitted'

    def _rate_dataset(self, url: str, data: dict) -> str:
        body = {
            "datasetId": data['datasetId'],
            "qualityRating": data['qualityRating'],
            "metadataRating": data['metadataRating']
        }
        self._http_client.request(HttpMethod.POST, url, body)
        return 'Submitted'

    def _get_dataset_rating_by_slug(self, url: str) -> str:
        return self._http_client.request(HttpMethod.GET, url=url)

    def _get_user_dataset_rating_by_slug(self, url: str) -> DatasetRatingList:
        result = self._http_client.request(HttpMethod.GET, url)
        return parse_obj_as(DatasetRatingList, result)

    def _search(self, url: str) -> List[SearchResult]:
        result = self._http_client.request(HttpMethod.GET, url)
        return parse_obj_as(List[SearchResult], result)

    def _create_metadata(self, url: str, data: DatasetMetadata):
        result = self._http_client.request(
            HttpMethod.POST, url=url, data=data.json(by_alias=True))
        return parse_obj_as(Dataset, result)

    def _get_privacy_violations(self, url: str) -> List[PrivacyViolation]:
        result = self._http_client.request(HttpMethod.GET, url)
        return parse_obj_as(List[PrivacyViolation], result)

    def _get_privacy_violation(self, url: str) -> PrivacyViolation:
        result = self._http_client.request(HttpMethod.GET, url)
        return parse_obj_as(PrivacyViolation, result)

    def _consider_privacy_violations(self, url: str) -> bool:
        self._http_client.request(HttpMethod.PUT, url)
        return True

    def _disregard_privacy_violations(self, url: str) -> bool:
        self._http_client.request(HttpMethod.PUT, url)
        return True

    def _get_access_permissions(self, url: str) -> List[AccessPermission]:
        result = self._http_client.request(HttpMethod.GET, url)
        return parse_obj_as(List[AccessPermission], result)

    def _get_access_permission(self, url: str) -> AccessPermission:
        result = self._http_client.request(HttpMethod.GET, url)
        return parse_obj_as(AccessPermission, result)

    def _approve_access_permissions(self, url: str) -> bool:
        self._http_client.request(HttpMethod.PUT, url)
        return True

    def _decline_access_permissions(self, url: str) -> bool:
        self._http_client.request(HttpMethod.PUT, url)
        return True

    def _get_latest_pending(self, url: str) -> Dataset:
        result = self._http_client.request(HttpMethod.GET, url)
        return parse_obj_as(Dataset, result)

    def _delete_resource(self, url: str) -> bool:
        self._http_client.request(HttpMethod.DELETE, url)
        return True

    def _update_dataset(self, url: str, data: dict) -> bool:
        self._http_client.request(HttpMethod.PUT, url, data)
        return True

    def _discard_dataset(self, url: str) -> bool:
        self._http_client.request(HttpMethod.PUT, url)
        return True

    def _publish_dataset(self, url: str) -> bool:
        self._http_client.request(HttpMethod.PUT, url)
        return True

    # TODO: extract filename
    # TODO: extract file type
    def _upload_file(self, url: str, file_name: str, file_type: str, file_path: str):
        with open(file_path, 'rb') as file:
            files = [
                ('files',
                 (file_name, file, file_type))
            ]
            result = self._http_client.request(
                HttpMethod.POST, url=url, files=files, headers={})

            return parse_obj_as(File, result[0])

    def _get_files(self, url: str) -> List[File]:
        result = self._http_client.request(HttpMethod.GET, url)
        return parse_obj_as(List[File], result)

    def _update_columns_metadata(sefl, url: str):
        pass

    def _create_file_indices(self, url: str, data: dict) -> bool:
        self._http_client.request(HttpMethod.POST, url, data)
        return True

    def _get_file_index(self, url: str) -> Index:
        result = self._http_client.request(HttpMethod.GET, url)
        return parse_obj_as(Index, result)

    def _get_file_errors(self, url: str) -> FileErrors:
        result = self._http_client.request(HttpMethod.GET, url)
        return parse_obj_as(FileErrors, result)

    def _update_cell_value(self, url: str, data: dict):
        pass
