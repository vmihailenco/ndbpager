#!/usr/bin/env python

from distutils.core import setup


version = __import__('ndbpager').get_version()
readme = open('README.rst').read()


setup(
    name='ndbpager',
    version=version.replace(' ', '-'),
    description='Pager for NDB',
    long_description=readme,
    author='Vladimir Mihailenco',
    author_email='vladimir.webdev@gmail.com',
    url='https://github.com/vmihailenco/ndbpager/',
    packages=['ndbpager'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
