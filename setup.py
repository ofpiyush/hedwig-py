from setuptools import setup
import os


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    # Nod to DRF for this function
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]

setup(name="hedwig-py",
      version="0.0.1",
      description="Python emitter and consumer for Hedwig",
      author="Piyush",
      author_email="piyush@magictiger.com",
      licesnse='MIT',
      packages=get_packages('hedwig'),
      install_requires=[
          'pika'
      ],
      test_requires=[
          'unittest',
          'requests'
      ],
      zip_safe=False)
