#!/usr/bin/env python

from distutils.core import setup


readme = open('README.md').read()


setup(
    name='ndbpager',
    version='0.1.1',
    description='Pager for NDB',
    long_description=readme,
    author='Vladimir Mihailenco',
    author_email='vladimir.webdev@gmail.com',
    url='https://github.com/vmihailenco/ndbpager/',
    packages=['ndbpager'],
    classifiers=[
        'Development Status :: 7 - Inactive',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
