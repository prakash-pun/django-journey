import requests
import urllib3
from bs4 import BeautifulSoup


def scrape_page_metadata(url):
    """Scrape target URL for metadata."""
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
    http = urllib3.PoolManager()

    # req = requests.get(url, headers=headers)
    response = http.request('GET', url)
    # html = BeautifulSoup(req.content, 'html.parser')
    html = BeautifulSoup(response.data, 'html.parser')
    metadata = {
        'title': get_title(html),
        'description': get_description(html),
        'image': get_image(html),
        'favicon': get_favicon(html, url),
        'sitename': get_site_name(html, url),
        'color': get_theme_color(html),
        'url': url
    }
    return metadata


def get_title(html):
    """Scrape page title."""
    title = None
    if html.title.string:
        title = html.title.string
    elif html.find("meta", property="og:title"):
        title = html.find("meta", property="og:title").get('content')
    elif html.find("meta", property="twitter:title"):
        title = html.find("meta", property="twitter:title").get('content')
    elif html.find("h1"):
        title = html.find("h1").string
    elif html.find_all("h1"):
        title = html.find_all("h1")[0].string
    if title:
        title = title.split('|')[0]
    return title


def get_description(html):
    """Scrape page description."""
    description = None
    if html.find("meta", property="description"):
        description = html.find("meta", property="description").get('content')
    elif html.find("meta", property="og:description"):
        description = html.find(
            "meta", property="og:description").get('content')
    elif html.find("meta", property="twitter:description"):
        description = html.find(
            "meta", property="twitter:description").get('content')
    elif html.find("p"):
        description = html.find("p").contents
    return description


def get_image(html):
    """Scrape share image."""
    image = None
    if html.find("meta", property="image"):
        image = html.find("meta", property="image").get('content')
    elif html.find("meta", property="og:image"):
        image = html.find("meta", property="og:image").get('content')
    elif html.find("meta", property="twitter:image"):
        image = html.find("meta", property="twitter:image").get('content')
    elif html.find_all("img", src=True):
        image = html.find_all("img")
        if image:
            image = html.find_all("img")[0].get('src')
    return image


def get_site_name(html, url):
    """Scrape site name."""
    if html.find("meta", property="og:site_name"):
        sitename = html.find("meta", property="og:site_name").get('content')
    elif html.find("meta", property='twitter:title'):
        sitename = html.find("meta", property="twitter:title").get('content')
    else:
        sitename = url.split('//')[1]
        return sitename.split('/')[0].rsplit('.')[1].capitalize()
    return sitename


def get_favicon(html, url):
    """Scrape favicon."""
    if html.find("link", attrs={"rel": "icon"}):
        favicon = html.find("link", attrs={"rel": "icon"}).get('href')
    elif html.find("link", attrs={"rel": "shortcut icon"}):
        favicon = html.find("link", attrs={"rel": "shortcut icon"}).get('href')
    else:
        favicon = f'{url.rstrip("/")}/favicon.ico'
    return favicon


def get_theme_color(html):
    """Scrape brand color."""
    if html.find("meta", property="theme-color"):
        color = html.find("meta", property="theme-color").get('content')
        return color
    return None
