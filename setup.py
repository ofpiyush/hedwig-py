from setuptools import setup
import os
import re


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    # Nod to DRF for this function
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]

setup(name="hedwig-py",
      version=get_version('hedwig'),
      description="Python emitter and consumer for Hedwig",
      url="https://github.com/ofpiyush/hedwig-py/",
      author="Piyush",
      author_email="mail@ofpiyush.in",
      license='MIT',
      packages=get_packages('hedwig'),
      install_requires=[
          'pika'
      ],
      zip_safe=False,
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Topic :: System :: Distributed Computing',
      ]
      )
