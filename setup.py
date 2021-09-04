# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='asoo',
    version='0.1.0',
    description='A CLI for extracting online shops products',
    long_description=readme,
    author='Mostafa Fekri',
    author_email='nilendd@gmail.com',
    url='https://github.com/nilend/asoo',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

