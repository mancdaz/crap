#!/usr/bin/env python

PROJECT = 'crap'

# Change docs/sphinx/conf.py too!
VERSION = '0.1'

# Bootstrap installation of Distribute
import distribute_setup
distribute_setup.use_setuptools()

from setuptools import setup, find_packages

#from distutils.util import convert_path
#from fnmatch import fnmatchcase
#import os
#import sys

try:
    long_description = open('README.rst', 'rt').read()
except IOError:
    long_description = ''

setup(
    name=PROJECT,
    version=VERSION,

    description='CLI to interact with rally',
    long_description=long_description,

    author='Darren Birkett',
    author_email='darren.birkett@gmail.com',

    url='https://github.com/mancdaz/crap',
    download_url='https://github.com/mancdaz/crap/tarball/master',

    classifiers=['Development Status :: 1 - Alpha',
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Intended Audience :: Developers',
                 'Environment :: Console',
                 ],

    platforms=['Any'],

    scripts=[],

    provides=[],
    install_requires=['distribute', 'cliff', 'pyral', 'requests==0.9.3'],

    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'crap = crap.main:main'
            ],
        'cliff.crap': [
            'task-show = crap.task:Show',
            'defect-show = crap.defect:Show',
            'story-show = crap.story:Show',
            'story-list = crap.story:List',
#            'two_part = cliffdemo.simple:Simple',
#            'error = cliffdemo.simple:Error',
#            'list files = cliffdemo.list:Files',
#            'files = cliffdemo.list:Files',
#            'file = cliffdemo.show:File',
#            'show file = cliffdemo.show:File',
            ],
        },

    zip_safe=False,
    )
