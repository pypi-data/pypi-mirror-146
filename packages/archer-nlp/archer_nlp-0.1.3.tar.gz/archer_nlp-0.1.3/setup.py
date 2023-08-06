#! -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='archer_nlp',
    version='0.1.3',
    description='archer nlp',
    long_description='',
    license='Apache License 2.0',
    url='https://github.com/beybin/archer_nlp',
    author='beybin',
    author_email='retry.happy@163.com',
    install_requires=["pandas>=1.4.1", "numpy>=1.19.3"],
    packages=find_packages()
)
