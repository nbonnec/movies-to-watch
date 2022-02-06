import logging

import SensCritique

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    movies = SensCritique.get_movies_and_providers()
    logging.debug(movies)

    # Print in markdown format
    for movie in movies:
        d = movie.get_dict()
        # FIXME manage multiple providers
        print('- **{title}** [<img src="{logo}" alt="provider-logo" style="width:20px;"/>]({provider})'.format(
            title=d['title'],
            logo=d['urls'][0]['logo'],
            provider=d['urls'][0]['provider']))
        print('    - {}'.format(d['synopsis']))
