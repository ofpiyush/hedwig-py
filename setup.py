from setuptools import setup

setup(name="hedwig-py",
      version="0.0.1",
      description="Python emitter and consumer for Hedwig",
      author="Piyush",
      author_email="piyush@magictiger.com",
      licesnse='MIT',
      packages=['hedwig'],
      install_requires=[
          'pika'
      ],
      test_requires=[
          'unittest',
          'requests'
      ],
      zip_safe=False)
