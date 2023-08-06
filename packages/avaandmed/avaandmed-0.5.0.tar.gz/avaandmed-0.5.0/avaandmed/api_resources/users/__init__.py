from avaandmed.http.http_client import HttpClient


class Users:
    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client
        self._me = None

    @property
    def me(self):
        if self._me is None:
            from avaandmed.api_resources.users.me import Me
            self._me = Me(self._http_client)
        return self._me
