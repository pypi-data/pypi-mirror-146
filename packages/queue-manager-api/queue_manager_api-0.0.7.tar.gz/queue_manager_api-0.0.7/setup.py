from distutils.core import setup
import os
from python_helper import StringHelper

print('''Installation on linux, run:
sudo apt install libpq-dev python3-dev
pip3.9 install --no-cache-dir python-framework --force --upgrade

Aliases:
sudo rm /usr/bin/python
sudo ln -s /usr/local/bin/pythonX.Y /usr/bin/python

sudo rm /usr/bin/pip
sudo ln -s /usr/local/bin/pipX.Y /usr/bin/pip
''')

VERSION = '0.0.7'

NAME = 'queue_manager_api'
API = 'api'
SRC = 'src'
LIBRARY = 'library'
RESOURCE = 'resource'
URL = f'https://github.com/SamuelJansen/{StringHelper.toSnakeCase(NAME)}/'

OS_SEPARATOR = os.path.sep

setup(
    name = NAME,
    packages = [
        API,
        f'{API}',
        f'{API}{OS_SEPARATOR}{SRC}',
        f'{API}{OS_SEPARATOR}{SRC}{OS_SEPARATOR}{LIBRARY}',
        f'{API}{OS_SEPARATOR}{SRC}{OS_SEPARATOR}{LIBRARY}{OS_SEPARATOR}annotation',
        f'{API}{OS_SEPARATOR}{SRC}{OS_SEPARATOR}{LIBRARY}{OS_SEPARATOR}constant',
        f'{API}{OS_SEPARATOR}{SRC}{OS_SEPARATOR}{LIBRARY}{OS_SEPARATOR}dto',
        f'{API}{OS_SEPARATOR}{SRC}{OS_SEPARATOR}{LIBRARY}{OS_SEPARATOR}enumeration',
        f'{API}{OS_SEPARATOR}{SRC}{OS_SEPARATOR}{LIBRARY}{OS_SEPARATOR}util',
        f'{API}{OS_SEPARATOR}{RESOURCE}'
    ],
    # data_files = [
    #     (STATIC_PACKAGE_PATH, [
    #         f'{RELATIVE_PATH}{OS_SEPARATOR}resource_1.extension',
    #         f'{RELATIVE_PATH}{OS_SEPARATOR}resource_2.extension'
    #     ])
    # ],
    version = VERSION,
    license = 'MIT',
    description = 'Queue Manager',
    author = 'Samuel Jansen',
    author_email = 'samuel.jansenn@gmail.com',
    url = URL,
    download_url = f'{URL}archive/v{VERSION}.tar.gz',
    keywords = ['queue', 'topic'],
    install_requires = [
        'python-framework<1.0.0,>=0.3.47',
        'globals<1.0,>=0.3.29',
        'python-helper<1.0,>=0.3.46'
    ],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7'
    ],
    python_requires='>=3.7'
)
