from typing import List


def build_endpoint(base_url: str, resources: List[str]):
    return f"{base_url}/{'/'.join(resources)}"
