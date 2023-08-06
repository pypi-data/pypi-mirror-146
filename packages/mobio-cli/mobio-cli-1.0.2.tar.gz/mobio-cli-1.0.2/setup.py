import os
import pathlib

from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

__PACKAGE_NAME__ = 'mobio_cli'
__TEMPLATE_DIR__ = 'templates'


def package_data_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        p = pathlib.Path(path)
        path = pathlib.Path(*p.parts[1:])
        for filename in filenames:
            paths.append(os.path.join(path, filename))
    return paths


data_files = package_data_files(os.path.join(__PACKAGE_NAME__, __TEMPLATE_DIR__))

setup(name='mobio-cli',
      version='1.0.2',
      author='MOBIO',
      author_email='contact@mobio.vn',
      description='Command line create Mobio\'s projects',
      long_description=long_description,
      long_description_content_type='text/markdown',
      entry_points={
          'console_scripts': [
              'mobio-cli = mobio_cli.__main__:main'
          ]
      },
      classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
      ],
      packages=find_packages(),
      package_data={'': data_files}
      )