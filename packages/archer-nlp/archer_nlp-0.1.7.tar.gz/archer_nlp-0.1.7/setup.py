#! -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='archer_nlp',
    version='0.1.7',
    description='archer nlp',
    long_description='',
    license='Apache License 2.0',
    url='https://github.com/beybin/archer_nlp',
    author='beybin',
    author_email='retry.happy@163.com',
    install_requires=["pandas", "numpy"],
    packages=find_packages()
)
