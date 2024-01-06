from urllib.parse import urlparse

from validators.url import url as url_validator


def validate(url):
    if not url_validator(url):
        return "Некорректный URL"
    elif len(url) > 255:
        return "URL превышает 255 символов"


def normalize(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}/"
