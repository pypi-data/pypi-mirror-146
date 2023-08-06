#!/usr/bin/env python
#:coding=utf-8:

import os
from setuptools import setup, find_packages

def read_file(filename):
    basepath = os.path.dirname(__file__)
    filepath = os.path.join(basepath, filename)
    with open(filepath) as f:
        read_text = f.read()
    return read_text


setup(
    name='bpnotify',
    version='0.48',
    description='Notification routing for Django',
    author='BeProud',
    author_email='project@beproud.jp',
    long_description=read_file('README.rst'),
    long_description_content_type="text/x-rst",
    url='https://github.com/beproud/bpnotify/',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.9',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.2',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    include_package_data=True,
    packages=find_packages(),
    namespace_packages=['beproud', 'beproud.django'],
    test_suite='tests.main',
    install_requires=[
        'Django>=2.2',
        'django-jsonfield>=1.0.1',
        'Celery>=4.2',
        'six',
    ],
    zip_safe=False,
)
