"""
Functions to access the SensCritique site.
"""

import logging
import requests
from bs4 import BeautifulSoup


class SensCritique:
    ROOT_URL = 'https://www.senscritique.com'
    TO_SEE_PAGE = ROOT_URL + '/NicoBobo/collection/wish/all/all/all/all/all/all/all/all/page-{}'

    def __init__(self, page=None):
        """
        Construct an instance with a page parsed.

        :param page: the page to parse, will be TO_SEE_PAGE if no parameter passed
        """
        # Get the first page
        if page is not None:
            with open(page) as html:
                self.soup = BeautifulSoup(html, 'html.parser')
        else:
            req = requests.get(SensCritique.TO_SEE_PAGE.format(1))

            if req.ok:
                logging.debug(req.text)
                self.soup = BeautifulSoup(req.text, 'html.parser')
            else:
                self.soup = BeautifulSoup()

    def get_page_count(self) -> int:
        """
        Get the number of pages in "Envies".
        :return: the count
        """
        pages = self.soup.find_all('a', 'eipa-anchor')

        count = 0
        for tag in pages:
            count = max(count, int(tag.attrs['data-sc-pager-page']))

        return count
