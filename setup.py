# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='acentoweb.competition',
      version=version,
      description="Create and manage photo, video, etc. competitions in Plone.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='plone competition ratings',
      author='Israel Saeta Pérez, sponsored by AcentoWeb S.L.',
      author_email='israel.saeta@dukebody.com',
      url='http://acentoweb.com',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['acentoweb'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'Plone',
          'plone.contentratings',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
