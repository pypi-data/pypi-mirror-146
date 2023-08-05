#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Martin Manns
# Distributed under the terms of the GNU General Public License

# --------------------------------------------------------------------
# py2svg is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# py2svg is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with py2svg.  If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------


from setuptools import setup, find_packages

from pys2svg import APP_NAME, VERSION

with open("README.md", "r", encoding='utf8') as readme_file:
    long_description = readme_file.read()

setup(
    name=APP_NAME,
    version=VERSION,
    author='Martin Manns',
    author_email='mmanns@gmx.net',
    description='pys2svg is a command line tool that converts pyspread'
                ' files in pys or pysu format into svg files.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pyspread.gitlab.io",
    project_urls={
        "Bug Tracker": "https://gitlab.com/pyspread/pys2svg/issues",
        "Source Code": "https://gitlab.com/pyspread/pys2svg",
    },
    packages=find_packages(),
    entry_points={
        'console_scripts': {
            'pyspread = pys2svg.pys2svg:main'
        }
    },
    package_data={'pys2svg': [
            'share/*',
            'share/*/*',
            'share/*/*/*',
            'share/*/*/*/*',
            'share/*/*/*/*/*',
        ]
    },
    license='GPL v3 :: GNU General Public License',
    keywords=['pyspread', 'pys', 'pysu', 'svg'],
    python_requires='>=3.6',
    requires=['pyspread (>=2.1)',
              'PyQt5 (>=5.10)',
              'markdown2 (>=2.3)'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Operating System :: Microsoft',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Office/Business :: Financial :: Spreadsheet',
        'Topic :: Multimedia :: Graphics :: Graphics Conversion',
    ],
)
