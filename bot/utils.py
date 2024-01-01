import requests
from urllib.parse import urlsplit, urlunsplit


def get_redicrect_url(url: str) -> str:
    resp = requests.get(url)
    if resp.history:
        return resp.url
    else:
        return url
    
def pure_bilibili_url(url: str) -> str:
    split_url = urlsplit(url)
    base_url = urlunsplit((split_url.scheme, split_url.netloc, split_url.path, '', ''))
    return base_url
    