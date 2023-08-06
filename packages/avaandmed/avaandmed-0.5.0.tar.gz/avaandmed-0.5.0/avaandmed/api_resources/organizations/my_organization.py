from typing import List

from pydantic.tools import parse_obj_as
from avaandmed.api_resources.datasets.dataset import Dataset
from avaandmed.api_resources.datasets.dataset_repository import DatasetRepository
from avaandmed.api_resources.organizations.organization import Organization
from avaandmed.http.http_client import HttpClient, HttpMethod
from avaandmed.api_resources.entities import (
    AccessPermission,
    DatasetMetadata,
    DatasetRatingList,
    File,
    FileErrors,
    Index,
    Preview,
    PrivacyViolation)
from avaandmed.utils import build_endpoint


class MyOrganization:
    """
    Controller class to handled Organizations endpoints. 
    """

    def __init__(self, id: str, http_client: HttpClient) -> None:
        self._http_client = http_client
        self._ENDPOINT = '/organizations/my-organizations'
        self._id = id
        self._dataset = None

    @property
    def dataset(self):
        if self._dataset is None:
            base_end_point = f"{self._ENDPOINT}/{self._id}/datasets"
            self._dataset = OrganizationDataset(
                base_end_point, self._http_client)
        return self._dataset

    def get_list_my_orgs(self) -> List[Organization]:
        """
        Retrieves list of organizations user belongs to.
        """
        url = self._ENDPOINT
        organizations_json = self._http_client.request(HttpMethod.GET, url=url)
        return parse_obj_as(List[Organization], organizations_json)

    def get_my_org_by_id(self, id: str) -> Organization:
        """
        Retrieves user's organization by ID.
        """
        url = f"{self._ENDPOINT}/{id}"
        organization = self._http_client.request(HttpMethod.GET, url=url)
        return parse_obj_as(Organization, organization)


class OrganizationDataset:
    def __init__(self, base_end_point: str, http_client: HttpClient) -> None:
        self._ENDPOINT = base_end_point
        self._dataset_repository = DatasetRepository(http_client)

    def get_by_id(self, id: str) -> Dataset:
        """
        Retrieve Dataset by its ID.
        """
        url = self.__build_url([id])
        return self._dataset_repository._get_dataset(url)

    def get_by_slug(self, slug: str) -> Dataset:
        """
        Retrieve Dataset by its slug name.
        """
        url = self.__build_url(['slug', slug])
        return self._dataset_repository._get_dataset(url)

    def get_dataset_list(self) -> List[Dataset]:
        """
        Retrieve list of all Datasets. Default limit is 20, but can be adjusted.
        """
        url = f"{self._ENDPOINT}"
        return self._dataset_repository._get_dataset_list(url)

    def get_file_rows_preview(self, id: str, file_id: str) -> Preview:
        """
        Preview file rows in the way, how end user will see them. 
        Returns object according to the provided data in the dataset's file.
        Returns Preview which is a type alias for List[Dict[str, Any]].
        """
        url = self.__build_url([id, 'files', file_id, 'preview'])
        return self._dataset_repository._get_file_rows_preview(url)

    def get_shared_datasets(self) -> List[Dataset]:
        """
        Retrieves list of Datasets shared with the user.
        """
        url = self.__build_url(['shared-with-me'])
        return self._dataset_repository._get_dataset_list(url)

    def get_all_privacy_violations(self) -> List[PrivacyViolation]:
        """
        Retrieves list of privacy violations related to user.
        """
        url = self.__build_url(['privacy-violations'])
        return self._dataset_repository._get_privacy_violations(url)

    def get_privacy_violation(self, id: str) -> PrivacyViolation:
        """
        Retrieves specific privacy violation by ID.
        """
        url = self.__build_url(['privacy-violations', id])
        return self._dataset_repository._get_privacy_violation(url)

    def consider_privacy_violation(self, id: str) -> bool:
        """
        Consider specific privacy violation by ID.
        Changes privacy violation;s status to Considered.
        """
        url = self.__build_url(['privacy-violations', id, 'consider'])
        return self._dataset_repository._consider_privacy_violations(url)

    def disregard_privacy_violtion(self, id: str) -> bool:
        """
        Disregard specific privacy violation by ID.
        Changes privacy violation's status to Disregarded.
        """
        url = self.__build_url(['privacy-violations', id, 'disregard'])
        return self._dataset_repository._disregard_privacy_violations(url)

    def get_all_access_permissions(self) -> List[AccessPermission]:
        """
        Retrieves list of all access permissions.
        """
        url = self.__build_url(['access-permissions'])
        return self._dataset_repository._get_access_permissions(url)

    def get_access_permission(self, id: str) -> AccessPermission:
        """
        Retrieves specific access permission by ID.
        """
        url = self.__build_url(['access-permissions', id])
        return self._dataset_repository._get_access_permission(url)

    def approve_access_permission(self, id: str) -> bool:
        """
        Approves specific access_permission by ID.
        """
        url = self.__build_url(['access-permissions', id, 'approve'])
        return self._dataset_repository._approve_access_permissions(url)

    def decline_access_permission(self, id: str) -> bool:
        """
        Declines specific access permission by ID.
        """
        url = self.__build_url(['access-permissions', id, 'decline'])
        return self._dataset_repository._decline_access_permissions(url)

    def get_latest_pending(self) -> Dataset:
        """
        Retrieves latest Dataset with pending status.
        """
        url = self.__build_url(['latest', 'pending'])
        return self._dataset_repository._get_latest_pending(url)

    def delete(self, id: str) -> bool:
        """
        Deletes specific Dataset by ID.
        """
        url = self.__build_url([id])
        return self._dataset_repository._delete_resource(url)

    # TODO: Typed data parameter instead of just dictionary
    def update(self, id: str, data: dict):
        url = self.__build_url([id])
        return self._dataset_repository._update_dataset(url, data)

    def discard(self, id: str) -> bool:
        """
        Set dataset status to "Discarded". 
        Dataset will not be useful anymore, but can be viewed.
        """
        url = self.__build_url([id, 'discard'])
        return self._dataset_repository._discard_dataset(url)

    def publish(self, id: str) -> bool:
        """
        Set dataset status to "Published".
        The dataset will be visible to the desired audience after publish.
        """
        url = self.__build_url([id, 'publish'])
        return self._dataset_repository._publish_dataset(url)

    # TODO
    # TODO: Typed data parameter instead of dictionary
    # BLOCKED: Unclear where to get file url value required by the endpoint
    def download(self, id: str, outfile: str, data: dict):
        url = self.__build_url([id, 'download-from-url'])
        return self._dataset_repository._download_file(url, outfile, data)

    def upload_file(self, dataset_id: str, file_name: str, file_type: str, file_path: str):
        """
        Uploads file for a specific dataset.
        Warning: File should be uploaded only after dataset was granted access status and license.
        """
        url = self.__build_url([dataset_id, 'upload'])
        return self._dataset_repository._upload_file(url, file_name, file_type, file_path)

    def get_all_files(self, id: str) -> List[File]:
        """
        Rertrieves list of all files related to specific Dataset.
        """
        url = self.__build_url([id, 'files'])
        return self._dataset_repository._get_files(url)

    # TODO
    # TODO: Typed data parameter instead of dictionary
    def update_column_metadata(self, id: str, file_id: str):
        """
        Used to set the column metadata, to improve dataset quality.
        """
        url = self.__build_url([id, 'files', file_id, 'columns', 'metadata'])
        return self._dataset_repository._update_columns_metadata(url)

    # TODO: Typed data parameter instead of dictionary
    def create_file_indices(self, id: str, file_id: str, data: dict) -> bool:
        """
        Creates indices to the file, to improve data quality.
        """
        url = self.__build_url([id, 'files', file_id, 'indices'])
        return self._dataset_repository._create_file_indices(url, data)

    def get_file_index(self, id: str, file_id: str) -> Index:
        """
        Retrieves all file indices.
        Returns Index class which contains list of different indices.
        """
        url = self.__build_url([id, 'files', file_id, 'indices'])
        return self._dataset_repository._get_file_index(url)

    def get_file_rows_with_errors(self, id: str, file_id: str) -> Preview:
        """
        Get processed file's rows that do not confirm to the constraints set by the information holder. 
        Useful during data quality improvements.
        Returns object according to the provided data in the dataset's file
        """
        url = self.__build_url([id, 'files', file_id])
        return self._dataset_repository._get_file_rows_preview(url)

    def delete_file(self, id: str, file_id: str) -> bool:
        """
        Deletes specific file for Dataset by ID.
        """
        url = self.__build_url([id, 'files', file_id])
        return self._dataset_repository._delete_resource(url)

    def get_file_errors(self, id: str, file_id: str) -> FileErrors:
        """
        Get all file's errors, which we found according to quality improvement rules.
        Returns object according to the provided data in the dataset's file.
        Returns FileErrors which is a type alias for List[Dict[str, Any]].
        """
        url = self.__build_url([id, 'files', file_id, 'errors'])
        return self._dataset_repository._get_file_errors(url)

    # TODO
    # BLOCKED: Weird 500 error
    def update_cell_value(self, id: str, file_id: str, data: dict):
        url = self.__build_url([id, 'files', file_id, 'row'])
        return self._dataset_repository._update_cell_value(url, data)

    def get_rating(self, slug: str) -> DatasetRatingList:
        """
        Retrieves different rating metrics for Dataset by its slug name.
        """
        url = self.__build_url([slug, 'ratings'])
        return self._dataset_repository._get_user_dataset_rating_by_slug(url)

    def create_dataset_metadata(self, metadata: DatasetMetadata) -> Dataset:
        """
        Create metadata for dataset. 
        This does not publishes dataset itself, but rather creates initial meta data. 
        To publish dataset using respective method.
        """
        url = self._ENDPOINT
        return self._dataset_repository._create_metadata(url, metadata)

    def __build_url(self, url_values: List[str]):
        return build_endpoint(self._ENDPOINT, url_values)
