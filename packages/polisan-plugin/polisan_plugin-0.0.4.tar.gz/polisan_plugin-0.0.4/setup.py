#!/usr/bin/env python

from io import open
from setuptools import setup
 
version="0.0.4"

with open("./README.md", encoding="utf-8") as f:
      long_description = f.read()

setup(name='polisan_plugin',
      version=version,
      license='MIT',
      author='LandaM',
      author_email='qwer.009771@gmail.com',
      description='Use this lib to build your plugins to polisan servers',
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=['polisan_plugin'],
      zip_safe=False)