from setuptools import setup, find_packages

setup(name='python-batian',
      version='0.1',
      description='Batian python client.',
      url='https://github.com/ishuah/python-batian',
      author='Ishuah Kariuki',
      author_email='kariuki@ishuah.com',
      licence='GNU GPLv3',
      install_requires=[
          'requests',
      ],
      packages=find_packages(exclude=("tests",)),
      zip_safe=False
      )
