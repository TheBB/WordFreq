#!/usr/bin/env python3

from distutils.core import setup

setup(
    name='WordFreq',
    version='0.1',
    description='Simple natural language word counter',
    author='Eivind Fonn',
    author_email='evfonn@gmail.com',
    license='MIT',
    url='https://github.com/TheBB/wordfreq',
    py_modules=['wordfreq'],
    entry_points={
        'console_scripts': [
            'wordfreq=wordfreq:wordfreq',
        ],
    },
    install_requires=['click', 'nltk'],
)
