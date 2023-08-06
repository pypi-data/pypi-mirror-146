import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '1.0.1'
PACKAGE_NAME = 'code_engine_client'
AUTHOR = 'moc-master'
AUTHOR_EMAIL = 'mocmaster123@163.com'
URL = 'https://github.com/moc-master/code_engine_client'

LICENSE = 'Apache License 2.0'
DESCRIPTION = 'a code engine of jimugaoshou bot which can control the motors of blocks'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
      'websocket-client',
      'grpcio'
]

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages()
      )