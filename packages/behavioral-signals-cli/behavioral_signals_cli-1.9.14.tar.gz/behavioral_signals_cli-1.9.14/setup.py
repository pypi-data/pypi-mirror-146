#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import sys
from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

requirements = [
    'aiofiles==0.6.0',
    'behavioral-signals-swagger-client-3==3.10.8',
    'chardet==3.0.4',
    'dotmap==1.3.8',
    'python-dateutil==2.8.0',
    'PyYAML==5.3.1',
    'ratelimit==2.2.1',
    'requests>=2.22.0',
    'ruamel.yaml==0.15.98',
    'tqdm==4.52.0'
]

if sys.version_info < (3, 5, 3):
    requirements += ['aiohttp==3.0.6']
else:
    requirements += ['aiohttp==3.7.3', 'aiodns==2.0.0', 'cchardet==2.1.7']


setup_requirements = [
    'pytest-runner',
    # TODO(behavioral-signals): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    'pytest',
    # TODO: put package test requirements here
]

setup(
    name='behavioral_signals_cli',
    version='1.9.14',
    description="Command Line Interface for Behavioral Signals Emotion and "
                "Behavior Recognition Engine in the Cloud",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Behavioral Signals",
    author_email='nassos@behavioralsignals.com',
    url="https://bitbucket.org/behavioralsignals/api-cli/src",
    download_url="https://bitbucket.org/behavioralsignals/api-cli/get/1.9.13.tar.gz",
    packages=find_packages(include=['behavioral_signals_cli']),
    entry_points={
        'console_scripts': [
            'behavioral_signals_cli=behavioral_signals_cli.cmd:main',
            'bsi-cli=behavioral_signals_cli.cmd:main',
            'bsi-meta=behavioral_signals_cli.synth:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='behavioral_signals_cli',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
