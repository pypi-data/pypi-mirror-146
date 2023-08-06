from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name = 'GenshinHarpPC',
    version = '0.0.4',
    keywords = ('Genshin', 'Harp'),
    description = 'just a simple test',
    license = 'MIT License',

    author = 'qwq20003',
    author_email = 'ysh01298@126.com',

    packages = find_packages(),
    platforms = 'any',

install_requires=['pypiwin32']
)