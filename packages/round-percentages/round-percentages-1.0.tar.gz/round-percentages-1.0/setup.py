from distutils.core import setup

from setuptools import find_packages

setup(
  name='round-percentages',
  packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests", "*tests.*"]),
  version='1.0',
  license='MIT',
  description='Round percentages that add up to 100, such that the rounded percentages also add up to 100 using the '
              'largest remainder method.',
  author='Si Anderson-Dry',
  author_email='simondo15@gmail.com',
  url='https://github.com/simondo92/round-percentages',
  keywords=['ROUND', 'PERCENTAGE'],
  install_requires=[],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
  ],
)
