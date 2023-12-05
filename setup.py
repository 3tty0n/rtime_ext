from setuptools import setup, find_packages

setup(
    name='rtime_ext',
    version='0.1.0',
    license='proprietary',
    description='Module Experiment',

    author='Yusuke Izawa',
    author_email='me@yizawa.com',
    url='https://www.yuiza.org',

    packages=find_packages(where='rtime_ext'),
    package_dir={'': 'rtime_ext'},
)
