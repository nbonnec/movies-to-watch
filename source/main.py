import logging

import SensCritique

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.debug(SensCritique.get_movies_and_providers())
