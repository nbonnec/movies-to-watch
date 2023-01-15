import logging
from typing import List

import SensCritique
from Types import Provider


def build_providers_string(p: List[Provider]) -> str:
    """
    Movies can have multiple providers (rarely).
    This function expect a dict of the form {'logo': 'src URL', 'provider': 'URL to the provider'}.
    :param p: the list of providers
    :return: a string with providers joined
    """
    provider_image_link = '[<img src="{logo}" alt="provider-logo" style="width:20px;"/>]({provider})'
    m = map(lambda x: provider_image_link.format(logo=x.logo_url, provider=x.work_url), p)
    return ' '.join([item for item in m])


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    movies = SensCritique.get_movies_and_providers()

    # Print in markdown format
    for work_info, url, providers, tv_release in movies:
        print(f'- **[{work_info.title}]({url})**', end='')

        if providers:
            print(f' {build_providers_string(providers)}', end='')
        if tv_release:
            print(f' {tv_release}', end='')

        print()
        print(f'    - {work_info.resume}')
