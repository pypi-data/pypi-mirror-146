#!/usr/bin/env python3
# +++{ coding:utf-8 }++++

from setuptools import setup, find_packages;
import pathlib;

here = pathlib.Path(__file__).parent.resolve();

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8');

# Setup all required for Silico to Python Library
setup(
    name='alice_ai',
    version='1.0.0',
    description='Artificial Intelligence with python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://maestroal.github.io/alice/',
    license='MIT License',
    author=[
        'A. Maestro Alvardo'
    ],
    author_email='maestroalvardo@gmail.com',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
    packages=find_packages(),
    keywords='Alice Python, Alice AI',
    python_requires='>=3, <4',
    install_requires=[
        'requests',
        'playsound',
        'gtts',
        'SpeechRecognition',
        'pyttsx3'
    ],
    entry_points={
        'console_scripts': [
            'aliceai=alice_ai.console:startConsole',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/maestroal/alice/issues',
        'Funding': 'https://donate.pypi.org',
        'Source': 'https://github.com/maestroal/alice/',
    },
);

# end line