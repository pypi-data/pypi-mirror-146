#!/usr/bin/env python


from setuptools import setup, find_packages

setup(
    name="pkradio",
    py_modules=['pkradio'],
    version="0.2",
    keywords=["pakistani", "urdu", "sindhi", "radio", "internet", "live"],
    description="Pakistani radio listener for a list stations, that'll hopefully keep growing.",
    long_description=open('README.md').read(),

    project_urls={
        'Homepage': 'https://www.techtum.dev/work-pkradio-220409.html',
        'Source': 'https://github.com/siphr/pkradio',
        'Tracker': 'https://github.com/siphr/pkradio/issues',
    },
    author="siphr",
    author_email="pypi@techtum.dev",

    packages=['pkradio'],
    package_data = {
        'pkradio':['stations.json']
        },
    platforms="any",
)
