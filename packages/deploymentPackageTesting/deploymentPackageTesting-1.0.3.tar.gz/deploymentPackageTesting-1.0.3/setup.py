from setuptools import setup, find_packages

setup(
    name='deploymentPackageTesting',
    version='1.0.3',
    author='Heorhii Yehiazarian',
    author_email='heorhii.yehiazarian@nextnano.com',
    description='simple package for testing purposes',
    packages=find_packages(exclude=["test"]),
    install_requires = ['numpy>=1.18']
)
