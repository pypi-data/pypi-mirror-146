import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
VERSION = '0.0.32'

INSTALL_REQUIRES = [
      'python-pptx',
      'dataclasses',
      'colour',
      'ddt==1.4.2',
      'openpyxl',
      ]

setup(
      version=VERSION,
      install_requires=INSTALL_REQUIRES,
      )