from typing import List, Optional
from avaandmed.api_resources import ApiResource
from avaandmed.api_resources.organizations.organization import Organization
from avaandmed.api_resources.users.user import User
from avaandmed.api_resources.entities import (
    Access,
    Category,
    Citation,
    Conformity,
    CoordinateReferenceSystem,
    File,
    Keyword,
    Licence,
    ProcessingStatus,
    Region,
    ResourceType,
    TopicCategory,
    UpdateIntervalUnit
)


class Dataset(ApiResource):
    """
    Class for representing Dataset model.
    """
    id: Optional[str]
    status: Optional[ProcessingStatus]
    slug: Optional[str]
    name: Optional[str]
    url: Optional[str]
    organization: Optional[Organization]
    organization_id: Optional[str]
    user: Optional[User]
    user_id: Optional[str]
    files: Optional[List[File]]
    keywords: Optional[List[Keyword]]
    categories: Optional[List[Category]]
    regions: Optional[List[Region]]
    coordinate_reference_systems: Optional[List[CoordinateReferenceSystem]]
    is_actual: Optional[bool]
    created_at: Optional[str]
    updated_at: Optional[str]
    name_et: Optional[str]
    name_en: Optional[str]
    description_et: Optional[str]
    description_en: Optional[str]
    maintainer: Optional[str]
    maintainer_email: Optional[str]
    maintainer_phone: Optional[str]
    citations: Optional[List[Citation]]
    conformities: Optional[List[Conformity]]
    south_latitude: Optional[str]
    north_latitude: Optional[str]
    west_longitude: Optional[str]
    east_longitude: Optional[str]
    language: Optional[str]
    licence: Optional[Licence]
    data_from: Optional[str]
    data_to: Optional[str]
    update_interval_unit: Optional[UpdateIntervalUnit]
    update_interval_frequency: Optional[int]
    access: Optional[Access]
    available_to: Optional[str]
    landing_page: Optional[str]
    qualified_attribution: Optional[str]
    was_generated_by: Optional[str]
    spatial_resolution: Optional[str]
    spatial_representation_type: Optional[str]
    spatial_data_service_type: Optional[str]
    geoportal_identifier: Optional[str]
    geoportal_keywords: Optional[str]
    lineage: Optional[str]
    pixel_size: Optional[str]
    resource_type: Optional[ResourceType]
    topic_categories: Optional[List[TopicCategory]]
    maturity: Optional[str]
    temporal_resolution: Optional[str]
    version_notes: Optional[str]
    parent_datasets: Optional[List['Dataset']]
    child_datasets: Optional[List['Dataset']]
    map_regions: Optional[List[str]]
    is_content_allowed: Optional[bool]


Dataset.update_forward_refs()
