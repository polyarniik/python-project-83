from bs4 import BeautifulSoup


def parse_page_data(response):
    data = {}

    data['status_code'] = response.status_code

    page = response.text
    soup = BeautifulSoup(page, "html.parser")

    data['title'] = soup.find("title").text[:255] if soup.find("title") else ""

    data['h1'] = soup.find("h1").text[:255] if soup.find("h1") else ""

    description = soup.find("meta", attrs={"name": "description"})
    data['description'] = description['content'][:255] if description else ''

    return data
