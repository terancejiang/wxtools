"""""""""""""""""""""""""""""
Project: wxtools
Author: Terance Jiang
Date: 1/16/2024
"""""""""""""""""""""""""""""
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='wxtools',
    version='0.1',
    packages=find_packages(),
    # install_requires=requirements,
)

entry_points = {
    'console_scripts': [
        'my_command=package_name.module:function',
    ],
},

author = 'JY',
author_email = 'your.email@example.com',
description = 'wxtools'
long_description = open('README.md').read(),
long_description_content_type = 'text/markdown',
url = '',
license = 'MIT',
classifiers = [
    'Programming Language :: Python :: 3.6',
    'License :: OSI Approved :: MIT License',
],
