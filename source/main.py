import logging

import SensCritique


def build_providers_string(p: SensCritique.Providers) -> str:
    """
    Movies can have multiple providers (rarely).
    This function expect a dict of the form {'logo': 'src URL', 'provider': 'URL to the provider'}.
    :param p: the list of providers
    :return: a string with providers joined
    """
    provider_image_link = '[<img src="{logo}" alt="provider-logo" style="width:20px;"/>]({provider})'
    m = map(lambda x: provider_image_link.format(logo=x[1], provider=x[0]), p)
    return ' '.join([item for item in m])


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    movies = SensCritique.get_movies_and_providers()

    # Print in markdown format
    for title_resume, providers in movies:
        print('- **[{title}]({endpoint})** {providers}'.format(title=title_resume[0], endpoint=providers[0],
                                                               providers=build_providers_string(providers)))
        print('    - {}'.format(title_resume[1]))
