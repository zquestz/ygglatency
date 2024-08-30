from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='ygglatency',
      version='0.2.3',
      description='Find the fastest Yggdrasil peers.',
      long_description=readme(),
      url='http://github.com/zquestz/ygglatency',
      author='quest',
      author_email='quest@mac.com',
      license='MIT',
      packages=['ygglatency'],
      install_requires=[
          'requests',
          'bs4',
          'icmplib'
      ],
      scripts=['bin/ygglatency'],
      zip_safe=False)