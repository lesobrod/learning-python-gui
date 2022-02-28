# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='learn_python_gui',
    version='1.1.0',
    description='Sample package for testing gui and matplotlib',
    long_description=readme,
    author='Sunik Denis',
    author_email='lesobrod@yandex.ru',
    url='https://github.com/lesobrod/learning-python-gui',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
