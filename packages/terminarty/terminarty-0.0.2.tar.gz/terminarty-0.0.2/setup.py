from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.0.2'
DESCRIPTION = 'A simple CLI helper for python'

# Setting up
setup(
    name='terminarty',
    version=VERSION,
    description=DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['colorama'],
    keywords=['terminal', 'cli', 'command-line', 'python', 'colored'],
    author='Artemon121',
    classifiers=[   
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3',
        'Operating System :: Unix',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
    ]
)
