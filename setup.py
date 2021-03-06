#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0', 'scikit-image>=0.15.0', 'scipy>=1.3.1', 'imagehash==4.0']

setup_requirements = [ ]

test_requirements = []

setup(
    author="Gurcan Gercek",
    author_email='gurcangercek@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="CLI tool to compare image similarities.",
    entry_points={
        'console_scripts': [
            'image_compare=image_compare.cli:main',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='image_compare',
    name='image_compare',
    packages=find_packages(include=['image_compare']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/ggercek/image_compare',
    version='1.0.0',
    zip_safe=False,
)
