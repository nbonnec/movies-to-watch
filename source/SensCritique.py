"""
Functions to access the SensCritique site.
"""

import logging
import requests
from bs4 import BeautifulSoup
from typing import List

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
    for i in range(1, get_page_count() + 1):
        page = requests.get(TO_SEE_PAGE.format(i))
        soup = BeautifulSoup(page.text, 'html.parser')
        list_of_movies.extend(map(lambda x: x['href'], soup.find_all('a', 'elco-anchor')))

    return list_of_movies


class MovieProviders:
    def __init__(self, movie_soup: BeautifulSoup, providers: list):
        self.title: str = movie_soup.title.text
        self.synopsis: str = movie_soup.find('meta', attrs={'name': 'description'})['content']
        urls = []
        for provider in providers:
            urls.append({'provider': provider['href'], 'logo': provider.find('img', 'product-providers__logo')['src']})
        self.providers_urls: List[dict] = urls

    def get_dict(self):
        return {'title': self.title, 'synopsis': self.synopsis, 'urls': self.providers_urls}


def get_movies_and_providers() -> List[MovieProviders]:
    """
    Fetch all movie pages and return the list of URLs to providers.
    :return: a list of the following dictionary:
            {'title': 'The title of the movie',
             'synopsis': 'The synopsis of the movie',
             'providers': [{'url': 'URL to the movie', 'logo': 'URL to the logo of the provider'}]
    """
    endpoints = [endpoint for endpoint in map(lambda x: ROOT_URL + x, get_movie_endpoints())]
    logging.debug(endpoints)
    movies_and_providers = []
    for endpoint in endpoints:
        request = requests.get(endpoint)
        if request.ok:
            soup = BeautifulSoup(request.text, 'html.parser')
            providers = soup.find_all('a', 'product-providers__item', 'href')
            if len(providers):
                movies_and_providers.append(MovieProviders(soup, providers))
    return movies_and_providers
