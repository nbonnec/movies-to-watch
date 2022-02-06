"""
Functions to access the SensCritique site.
"""

import logging
import requests
from bs4 import BeautifulSoup

ROOT_URL = 'https://www.senscritique.com'
TO_SEE_PAGE = ROOT_URL + '/NicoBobo/collection/wish/all/all/all/all/all/all/all/all/page-{}'


def _get_soup(page=None) -> BeautifulSoup:
    # Get the first page
    if page is not None:
        with open(page) as html:
            soup = BeautifulSoup(html, 'html.parser')
    else:
        req = requests.get(TO_SEE_PAGE.format(1))

        if req.ok:
            soup = BeautifulSoup(req.text, 'html.parser')
        else:
            soup = BeautifulSoup()
    return soup


def get_page_count() -> int:
    """
    Get the number of pages in "Envies".
    :return: the count
    """
    pages = _get_soup().find_all('a', 'eipa-anchor')

    count = 0
    for tag in pages:
        count = max(count, int(tag.attrs['data-sc-pager-page']))

    return count


def get_movie_endpoints() -> list:
    """
    Get all the urls of the movies across all pages.
    :return: a list of urls
    """
    list_of_movies = []
    for i in range(1, get_page_count()):
        page = requests.get(TO_SEE_PAGE.format(i))
        soup = BeautifulSoup(page.text, 'html.parser')
        list_of_movies.extend(map(lambda x: x['href'], soup.find_all('a', 'elco-anchor')))

    return list_of_movies


def get_movies_and_providers() -> list:
    """
    Fetch all movie pages and return the list of URLs to providers.
    :return: a list of URLs
    """
    endpoints = [endpoint for endpoint in map(lambda x: ROOT_URL + x, get_movie_endpoints())]
    logging.debug(endpoints)
    provider_a = []
    for endpoint in endpoints:
        request = requests.get(endpoint)
        if request.ok:
            soup = BeautifulSoup(request.text, 'html.parser')
            provider_a.extend(soup.find_all('a', 'product-providers__item', 'href'))
    return [url for url in map(lambda x: x['href'], provider_a)]
