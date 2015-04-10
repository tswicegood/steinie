import sys
if sys.argv[1] == 'develop':
    from setuptools import setup
else:
    from distutils.core import setup

setup(
    name='steinie',
    version='1.0.1',
    author='Travis Swicegood',
    author_email='development@domain51.com',
    description='A little framework for doing web applications',
    long_description=open("./README.rst").read(),
    packages=['steinie', ],
    install_requires=[
        'werkzeug>=0.10.1',
    ],
    include_package_data=True,
    zip_safe=False,
)
