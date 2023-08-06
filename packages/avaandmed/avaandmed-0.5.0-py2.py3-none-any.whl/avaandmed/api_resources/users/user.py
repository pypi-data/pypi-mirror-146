from typing import Optional
from avaandmed.api_resources import ApiResource


class User(ApiResource):
    """
    Represents User model.
    """
    id: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    slug: Optional[str]
    email: Optional[str]
    name: Optional[str]
