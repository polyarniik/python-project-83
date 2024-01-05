from validators.url import url as url_validator


def validate(url):
    if not url_validator(url):
        return "Некорректный URL"
    elif len(url) > 255:
        return "URL превышает 255 символов"
