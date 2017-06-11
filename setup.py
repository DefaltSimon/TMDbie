# coding=utf-8
from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()


extras = {
    "fast": ["ujson>=1.35"],
    "requests": ["requests>=2.13.0"]
}

setup(name='TMDbie',
      version='1.1.1',
      description='Python API wrapper for The Movie Database',
      classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.5',
          'Intended Audience :: Developers',
      ],
      url='https://github.com/DefaltSimon/TMDbie',
      author='DefaltSimon',
      license='MIT',
      keywords="defaltsimon tmdb movies api wrapper",
      packages=['tmdbie'],
      install_requires=requirements,
      extras_require=extras,
      zip_safe=False)
