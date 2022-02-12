"""
Functions to access the SensCritique site.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Tuple, Optional

ROOT_URL = 'https://www.senscritique.com'
DESIRES_PAGE = ROOT_URL + '/NicoBobo/collection/wish/all/all/all/all/all/all/all/all/page-{}'
DESIRES_PAGE_1 = ROOT_URL + '/NicoBobo/collection/wish/all/all/all/all/all/all/all/all/page-{}'.format(1)


def _get_soup_from_page(page: str) -> BeautifulSoup:
    """
    Get soup from a HTML page.

    :param page: the page to soup
    :return: the soup with the good parser
    """
    return BeautifulSoup(page, 'html.parser')


def _get_soup_from_url(url: str) -> BeautifulSoup:
    """
    Get the soup from an URL. Will access the web via a Request.

    :param url: the URL to access
    :return: the soup
    """
    req = requests.get(url)
    if req.ok:
        soup = _get_soup_from_page(req.text)
    else:
        soup = BeautifulSoup()
    return soup


def _extract_desires_page_count(soup: BeautifulSoup) -> int:
    """
    Get the count of pages in "Envies".

    :param soup: the "Envies" page soup where to search
    :return: the count
    """
    tags = soup.find_all('a', 'eipa-anchor')

    def get_page_number_in_tag(tag): return int(tag.attrs['data-sc-pager-page'])

    page_number_tag = max(tags, key=get_page_number_in_tag)

    return get_page_number_in_tag(page_number_tag)


def get_desire_movies_urls() -> list:
    """
    Get all the urls of the movies across all pages.
    :return: a list of urls
    """
    page_count = _extract_desires_page_count(_get_soup_from_url(DESIRES_PAGE_1)) + 1
    list_of_movies = []
    for i in range(1, page_count):
        request = requests.get(DESIRES_PAGE.format(i))
        if request.ok:
            soup = _get_soup_from_page(request.text)
            list_of_movies.extend(map(lambda x: ROOT_URL + x['href'], soup.find_all('a', 'elco-anchor')))

    return list_of_movies


class MovieItem:
    def __init__(self, endpoint: str, movie_soup: BeautifulSoup, providers: list):
        self.endpoint: str = endpoint

        # join and split to clean texts
        self.title: str = ' '.join(movie_soup.title.text.split())
        self.resume: str = ' '.join(movie_soup.find('p', 'pvi-productDetails-resume').text.split()).replace(
            'Lire la suite', '')

        urls = []
        for provider in providers:
            urls.append({'provider': provider['href'], 'logo': provider.find('img', 'product-providers__logo')['src']})
        self.providers_urls: List[dict] = urls

    def get_dict(self):
        return {'title': self.title, 'endpoint': self.endpoint, 'resume': self.resume, 'urls': self.providers_urls}


Providers = List[Tuple[str, str]]
TitleAndResume = Tuple[str, str]


def _extract_providers(soup: BeautifulSoup) -> Optional[Providers]:
    """
    Get the providers in the soup.

    :param soup: the soup of a movie
    :return: a list of one or more providers and their logo
    """
    providers = soup.find_all('a', 'product-providers__item', 'href')
    if len(providers):
        def extract(x):
            return x['href'], x.find('img', 'product-providers__logo')['src']

        return [url for url in map(extract, providers)]
    else:
        return []


def _extract_title_and_resume(soup: BeautifulSoup) -> TitleAndResume:
    """
    Get and clean title and resume from the soup.

    :param soup: the soup of a movie
    :return: both title and resume as a text
    """
    title = ' '.join(soup.title.text.split()) if soup.title is not None else 'No title'
    resume_tag = soup.find('p', 'pvi-productDetails-resume')
    resume = ' '.join(resume_tag.text.split()).replace('Lire la suite', '') if resume_tag is not None else 'No resume'
    return title, resume


def _extract_tv_release(soup: BeautifulSoup) -> Optional[str]:
    tag = soup.find('li', 'pvi-tvRelease')
    return ' '.join(tag.text.split()) if tag is not None else None


def get_movies_and_providers() -> zip(TitleAndResume, List[str], Providers, List[str]):
    """
    Fetch all movie pages and return the list of URLs to providers.

    :return: a zip with Providers and TitleAndResume
    """
    sc_urls: List[str] = []
    providers: [Providers] = []
    title_and_resumes: List[TitleAndResume] = []
    tv_release = []
    for url in get_desire_movies_urls():
        request = requests.get(url)
        if request.ok:
            soup = _get_soup_from_page(request.text)

            prov = _extract_providers(soup)
            tv = _extract_tv_release(soup)

            if prov or tv:
                title_and_resumes.append(_extract_title_and_resume(soup))
                sc_urls.append(url)
                providers.append(prov)
                tv_release.append(tv)

    return zip(title_and_resumes, sc_urls, providers, tv_release)
