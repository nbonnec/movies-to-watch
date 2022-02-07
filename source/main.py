import logging

import SensCritique
from typing import List


def build_providers_string(providers: List[dict]) -> str:
    """
    Movies can have multiple providers (rarely).
    This function expect a dict of the form {'logo': 'src URL', 'provider': 'URL to the provider'}.
    :param providers: the list of providers
    :return: a string with providers joined
    """
    provider_image_link = '[<img src="{logo}" alt="provider-logo" style="width:20px;"/>]({provider})'
    m = map(lambda x: provider_image_link.format(logo=x['logo'], provider=x['provider']), providers)
    return ' '.join([item for item in m])


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    movies = SensCritique.get_movies_and_providers()

    # Print in markdown format
    for movie in movies:
        d = movie.get_dict()
        print('- **[{title}]({endpoint})** {providers}'.format(title=d['title'], endpoint=d['endpoint'],
                                                               providers=build_providers_string(d['urls'])))
        print('    - {}'.format(d['resume']))
