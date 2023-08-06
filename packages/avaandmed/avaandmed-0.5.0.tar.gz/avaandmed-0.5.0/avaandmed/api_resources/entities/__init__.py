from datetime import datetime
from typing import Any, Dict, List, Optional
from enum import Enum

from pydantic import Field
from avaandmed.api_resources import ApiResource
from avaandmed.api_resources.users.user import User


class KeywordEmsCategory(ApiResource):
    id: int
    ems_category_id: int
    keyword_id: int


class Keyword(ApiResource):
    """
    Handles keywords serialization in Dataset model.
    """
    id: int
    name: str
    language: str
    keyword_ems_category: KeywordEmsCategory


class Citation(ApiResource):
    """
    Handles citations serialization in Dataset model.
    """
    url: str
    name: str


class Conformity(ApiResource):
    """
    Handles conformities serialization in Dataset model.
    """
    release_date: str
    specification: str


class Licence(ApiResource):
    """
    Handles licences serialization.
    """
    id: str
    name: str
    description: str
    code: Optional[str]
    identifier: Optional[str]


class CoordinateReferenceSystem(ApiResource):
    """
    Handles coordinateReferenceSystems serialization in Dataset model.
    """
    id: int
    uri: str


class Category(ApiResource):
    """
    Handles categories serialization.
    """
    id: int
    name: str
    description: Optional[str]
    ems_ids: Optional[List[int]]


class EmsCategory(ApiResource):
    """
    Handles Ems categories serialization.
    """
    id: int
    name: str


class Region(ApiResource):
    """
    Handles regions serialization.
    """
    id: int
    name: str
    coordinates: Optional[str]


class ProcessingStatus(Enum):
    NONE = 'none'
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'


class File(ApiResource):
    """
    Handles files field serialization in Dataset model.
    """
    id: str
    name: str
    mimetype: str
    size: str
    dataset_id: str
    metadata: Dict[str, Any]
    processing_status: ProcessingStatus
    storage_filename: str


class UpdateIntervalUnit(str, Enum):
    """
    Handles updateIntervalUnit field deserialization in Dataset model.
    Serializaes into Enum i.e UpdateIntervalUnit.MINUTE.
    """
    CONTINUAL = 'continual'
    MINUTE = 'minute'
    WORKDAY = 'workday'
    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'
    QUARTER = 'quarter'
    YEAR = 'year'
    AS_NEEDED = 'asNeeded'
    IRREGULAR = 'irregular'
    NOT_PLANNED = 'notPlanned'
    UNKNOWN = 'unknown'
    NEVER = 'never'


class Access(str, Enum):
    """
    Handles access field serialization in Dataset model.
    Serializes into Enum i.e Access.PUBLIC
    """
    PUBLIC = 'public'
    PROTECTED = 'protected'
    PRIVATE = 'private'


class ResourceType(str, Enum):
    """
    Handles resourceType field serialization in Dataset model.
    Serializes into Enum i.e ResourceType.DATASET
    """
    DATASET = 'dataset'
    SERIES = 'series'
    SERVICE = 'service'


class TopicCategory(str, Enum):
    """
    Handles topicCategores field serialization in Dataset model.
    Seriliazles into Enum i.e TopicCategoty.BIOTA
    """
    BIOTA = 'biota'
    BOUNDARIES = 'boundaries'
    CLIMATOLOGY_METEROROLOGY_ATMOSPHERE = 'climatologyMeteorologyAtmosphere'
    ECONOMY = 'economy'
    ELEVATION = 'elevation'
    ENVIRONMENT = 'environment'
    FARMING = 'farming'
    GEO_SCIENTIFIC_INFORMATION = 'geoscientificInformation'
    HEALTH = 'health'
    IMAGERY_BASE_MAPS_EARTH_COVER = 'imageryBaseMapsEarthCover'
    INLAND_WATERS = 'inlandWaters'
    INTELLIGENCE_MILITARY = 'intelligenceMilitary'
    LOCATION = 'location'
    OCEANS = 'oceans'
    PLANNING_CADASTRE = 'planningCadastre'
    SOCIETY = 'society'
    STRUCTURE = 'structure'
    TRANSPORTATION = 'transportation'
    UTILITIES_COMMUNICATIOn = 'utilitiesCommunication'


class Notification(str, Enum):
    """
    Handles notificaitons field serialization in Organization model.
    """
    DATASET_COMMENTED = 'DATASET_COMMENTED'
    DATASET_RATED = 'DATASET_RATED'
    DATASET_ACCESS_REQUEST = 'DATASET_ACCESS_REQUEST'
    DATA_WISH_NEW = 'DATA_WISH_NEW'
    DATASET_PRIVACY_VIOLATION = 'DATASET_PRIVACY_VIOLATION'


class FileColumn(ApiResource):
    """
    Handles field serialization from /columns endpoint.
    """
    column: Optional[str]
    type: Optional[str]
    description: Optional[str]
    api_field_name: Optional[str]
    unit: Optional[str]
    required: Optional[bool]
    private: Optional[bool]
    unique: Optional[bool]


class InformationHolder(ApiResource):
    slug: str
    name: str


class SearchResult(ApiResource):
    """
    Handles search results serialization.
    """
    id: Optional[str]
    slug: Optional[str]
    name: Optional[str]
    name_et: Optional[str]
    name_en: Optional[str]
    description: Optional[str]
    description_et: Optional[str]
    description_en: Optional[str]
    information_holder: Optional[InformationHolder]
    update_interval_frequency: Optional[int]
    update_interval_unit: Optional[UpdateIntervalUnit]
    created_at: Optional[str]
    updated_at: Optional[str]
    keywords: Optional[List[str]]
    keywords_et: Optional[List[str]]
    keywords_en: Optional[List[str]]
    categories: Optional[List[str]]
    categories_et: Optional[List[str]]
    categories_en: Optional[List[str]]


Preview = List[Dict[str, Any]]


class PartialDatasetInfo(ApiResource):
    id: Optional[str]
    name_et: Optional[str]
    name_en: Optional[str]
    slug: Optional[str]
    organiztion_id: Optional[str]
    user_id: Optional[str]
    name: Optional[str]


class Inquiry(ApiResource):
    id: Optional[str]
    user_id: Optional[str]
    description: Optional[str]
    dataset_id: Optional[str]
    status: ProcessingStatus
    created_at: Optional[str]
    dataset: Optional[PartialDatasetInfo]
    user: Optional[User]
    seen: Optional[bool]


PrivacyViolation = Inquiry
AccessPermission = Inquiry


class Polynomial(ApiResource):
    id: int
    column: str


class Identifier(ApiResource):
    id: int
    column: str
    identifier: str


class Index(ApiResource):
    polynomial: List[Polynomial]
    identifier: List[Identifier]


FileErrors = List[Dict[str, Any]]


class DatasetRating(ApiResource):
    id: int
    quality_rating: Optional[int]
    metadata_rating: Optional[int]
    description: Optional[str]


DatasetRatingList = List[DatasetRating]


class Language(ApiResource):
    code: str
    name: str


class KeywordInfo(ApiResource):
    id: int
    name: str
    ems_id: Optional[str]


class DatasetMetadata(ApiResource):
    name_et: str = Field(...)
    name_en: str = Field(...)
    description_et: str = Field(...)
    description_en: str = Field(...)
    maintainer: str = Field(...)
    maintainer_email: str = Field(...)
    maintainer_phone: str = Field(...)
    # TODO: Find a way to map ids to actual values
    keyword_ids: List[int] = Field(...)
    # TODO: Find a way to map ids to actual values
    category_ids: List[int] = Field(...)
    # TODO: Find a way to map ids to actual values
    region_ids: List[int] = Field(...)
    data_from: datetime = Field(...)
    available_to: datetime = Field(...)
    update_interval_unit: UpdateIntervalUnit = Field(...)
    update_interval_frequency: int = Field(...)
    # optional fields
    conformities: Optional[List[Conformity]] = []
    lineage: Optional[str]
    spatial_representation_type: Optional[str]
    spatial_data_service_type: Optional[str]
    topic_categories: Optional[List[TopicCategory]] = []
    pixel_size: Optional[int]
    coordinate_reference_system_ids: Optional[List[int]] = []
    south_latitude: Optional[str]
    north_latitude: Optional[str]
    west_longitude: Optional[str]
    east_longitude: Optional[str]
    language: Optional[str]
    qualified_attribution: Optional[str]
    was_generated_by: Optional[str]
    spatial_resolution: Optional[str]
    temporal_resolution: Optional[str]
    maturity: Optional[str]
    parent_dataset_ids: Optional[List[str]]
    child_dataset_ids: Optional[List[str]]
    version_notes: Optional[str]
    data_to: Optional[datetime]
    landing_page: Optional[str]
    resource_type: Optional[ResourceType]
