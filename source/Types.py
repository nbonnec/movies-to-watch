"""
Some types used by the application.
"""

from typing import NamedTuple, List


class Provider(NamedTuple):
    """
    A provider is a tuple of two URLs: one for the work itself on the platform, another for the logo of the platform.
    """
    work_url: str
    logo_url: str


class WorkInfo(NamedTuple):
    """
    Information about the work. For now it is only the title and the resume.
    """
    title: str
    resume: str


Providers = List[Provider]
""" A list of providers. """
