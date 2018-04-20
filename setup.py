#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0', 'Flask_MySQLdb>=0.2.0']

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Hugh O'Brien",
    author_email='hugh.obrien@ucdconnect.ie',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="A script used to datamine the JCDecaux API for Dublin Bike data",
    entry_points={
        'console_scripts': [
            'miner=dublinbikeminer.dublinbikeminer:main',
            'flaskapp=dublinbikeminer.flaskapp:main'
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='dublinbikeminer',
    name='dublinbikeminer',
    packages=find_packages(include=['dublinbikeminer']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/OBrien1510/dublinbikeminer',
    version='0.1.0',
    zip_safe=False,
)
