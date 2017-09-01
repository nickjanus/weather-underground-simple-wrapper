import sys


try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup


if sys.version_info <= (3, 6):
  error = 'Requires Python Version 3.6 or above... exiting.'
  print >> sys.stderr, error
  sys.exit(1)


requirements = []

setup(name='weather-underground-simple-wrapper',
      version='2.4-dev',
      description='Python client library for Weather Underground API',
      scripts=[],
      url='https://github.com/benrhere/weather-underground-simple-wrapper/',
      packages=['WeatherUndergroundSimpleWrapper'],
      license='MIT',
      setup_requires=requirements,
      install_requires=requirements,
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 3.6',
                   'Topic :: Internet',
                   ]
      )
