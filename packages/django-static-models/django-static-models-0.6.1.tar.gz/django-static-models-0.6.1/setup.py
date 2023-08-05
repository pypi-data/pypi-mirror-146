#!/usr/bin/env python
# setup.py generated by flit for tools that don't yet use PEP 517

from distutils.core import setup

packages = \
['static_models']

package_data = \
{'': ['*'],
 'static_models': ['management/*', 'management/commands/*', 'tests/*']}

setup(name='django-static-models',
      version='0.6.1',
      description='Generate static pages from views',
      author='robert crowther',
      author_email='rw.crowther@gmail.com',
      url='https://github.com/rcrowther/django-static_models',
      packages=packages,
      package_data=package_data,
     )
