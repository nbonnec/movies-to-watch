import logging

import SensCritique

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    sc = SensCritique.SensCritique()
    logging.debug(sc.get_page_count())
    logging.debug(sc.get_movie_urls())
