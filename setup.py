# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from sixel import __version__, __license__, __author__
import inspect, os

filename = inspect.getfile(inspect.currentframe())
dirpath = os.path.abspath(os.path.dirname(inspect.getfile(inspect.currentframe())))
long_description = open(os.path.join(dirpath, "README.md")).read()

setup(name                  = 'sixel',
      version               = __version__,
      description           = ('View full-pixel color graphics on Sixel-supported terminals'),
      long_description      = long_description,
      py_modules            = ['sixel'],
      eager_resources       = [],
      classifiers           = ['Development Status :: 4 - Beta',
                               'Topic :: Terminals',
                               'Environment :: Console',
                               'Intended Audience :: End Users/Desktop',
                               'License :: OSI Approved :: GNU General Public License (GPL)',
                               'Programming Language :: Python'
                               ],
      keywords              = 'sixel terminal image',
      author                = __author__,
      author_email          = 'lubosz@gmail.com',
      url                   = 'https://github.com/lubosz/python-sixel',
      license               = __license__,
      packages              = find_packages(exclude=[]),
      zip_safe              = False,
      include_package_data  = False,
      install_requires      = ['Pillow'],
      entry_points          = """
                              [console_scripts]
                              sixelconv = sixel:main
                              """
      )

