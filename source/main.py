import logging

import SensCritique

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    sc = SensCritique.SensCritique('../resources/html/page-1.html')
    logging.debug(sc.get_page_count())
