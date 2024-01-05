from validators.url import url as url_validator


def validate(url):
    if not url_validator(url):
        return "Wrong URL"
    elif len(url) > 255:
        return "The URL exceeds 255 characters"
