from pydantic import BaseModel


def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


class ApiResource(BaseModel):
    """
    An abstract class for all the entities used in the module.
    Here is defined common properties that are used among all entities.
    """

    class Config:
        alias_generator = to_camel_case
