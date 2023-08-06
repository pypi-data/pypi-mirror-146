from typing import Optional, List, Any
from avaandmed.api_resources.entities import Notification
from avaandmed.api_resources import ApiResource
from avaandmed.api_resources.organizations.organization_user import OrgUser


class Organization(ApiResource):
    """
    Represents Organization enitity.
    """
    id: Optional[str]
    reg_code: Optional[str]
    name: Optional[str]
    slug: Optional[str]
    contact: Optional[str]
    contact_email: Optional[str]
    description: Optional[str]
    is_public_body: Optional[bool]
    notifications: Optional[List[Notification]]
    org_user: Optional[OrgUser]
    domain: Optional[str]
    image: Optional[Any]  # TODO
