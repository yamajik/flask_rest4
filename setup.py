#!/usr/bin/env python

"""
Flask-REST4
-------------
Elegant RESTful API for your Flask apps.
"""
from setuptools import setup, find_packages


setup(
    name='flask_rest4',
    version='0.3.2',
    packages=find_packages(),
    url='https://github.com/squirrelmajik/flask_rest4',
    license='See License',
    author='majik',
    author_email='me@yamajik.com',
    description='Elegant RESTful API for your Flask apps.',
    long_description=__doc__,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
