from typing import Optional
from avaandmed.api_resources import ApiResource


class OrgUser(ApiResource):
    id: Optional[str]
    organization_id: Optional[str]
    user_id: Optional[str]
    user_job_title: Optional[str]
    user_role: Optional[str]
    user_domain: Optional[str]
    user_role_valid_from: Optional[str]
    user_role_valid_to: Optional[str]
