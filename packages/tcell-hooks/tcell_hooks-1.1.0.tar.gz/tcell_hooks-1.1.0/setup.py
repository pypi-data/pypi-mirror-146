from setuptools import setup, find_packages
from tcell_hooks.version import VERSION

try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='tcell_hooks',
    version=VERSION,
    description='Allows custom event sending of login failures/success to TCell',
    url='https://www.rapid7.com/products/tcell/',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Rapid7',
    license='No License',
    install_requires=[],
    tests_require=[],
    packages=find_packages()
)
