import source.SensCritique
import unittest
import os
from bs4 import BeautifulSoup

SC = source.SensCritique
"""Type alias."""

FILE_PATH = os.path.dirname(__file__)
RESOURCES_FOLDER = FILE_PATH + '/../resources/html/'


def _get_soup_from_file(path: str) -> BeautifulSoup:
    with open(path, 'r') as f:
        return BeautifulSoup(f.read(), 'html.parser')


class TestSensCritique(unittest.TestCase):

    def test_get_count(self) -> None:
        soup = _get_soup_from_file(RESOURCES_FOLDER + 'page-1.html')
        self.assertEqual(SC._extract_desires_page_count(soup), 9)

    def test_extract_providers(self) -> None:
        soup = _get_soup_from_file(RESOURCES_FOLDER + 'victoria.html')
        urls = SC._extract_providers(soup)
        self.assertEqual(urls, [
            ("https://www.netflix.com/title/80043050", "https://static.senscritique.com/img/providers/netflix.png"),
            ("https://www.ocs.fr/programme/VICTORIAXXXW0105536",
             "https://static.senscritique.com/img/providers/ocs.png")])

        soup = _get_soup_from_file(RESOURCES_FOLDER + 'tucker-and-dale.html')
        urls = SC._extract_providers(soup)
        self.assertEqual(urls, [])

        soup = _get_soup_from_file(RESOURCES_FOLDER + 'certains-laiment-chaud.html')
        urls = SC._extract_providers(soup)
        self.assertEqual(urls, [])

    def test_extract_title_and_resume(self) -> None:
        soup = _get_soup_from_file(RESOURCES_FOLDER + 'victoria.html')
        title, resume = SC._extract_title_and_resume(soup)
        self.assertEqual(title, 'Victoria - Film (2015) - SensCritique')
        self.assertEqual(resume,
                         'Victoria, espagnole fraîchement débarquée à Berlin, rencontre un groupe d\'amis.'
                         ' Elle décide de les suivre se laissant entraîner par la fête jusqu\'au dérapage.')

    def test_extract_tv_release(self) -> None:
        soup = _get_soup_from_file(RESOURCES_FOLDER + 'tucker-and-dale.html')
        release = SC._extract_tv_release(soup)
        self.assertEqual(release, None)

        soup = _get_soup_from_file(RESOURCES_FOLDER + 'certains-laiment-chaud.html')
        release = SC._extract_tv_release(soup)
        self.assertEqual(release, 'mercredi 16 février sur Ciné+ Classic à 20:50')


if __name__ == '__main__':
    unittest.main()
