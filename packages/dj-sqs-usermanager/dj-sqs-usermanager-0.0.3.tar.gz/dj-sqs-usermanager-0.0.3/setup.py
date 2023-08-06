import os

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="dj-sqs-usermanager",
    version="0.0.3",
    packages=find_packages(),
    include_package_data=True,
    license="MIT",
    description="Auto Add User to SQS Queue for microservices",
    long_description=README,
    url="https://vert-capital.com/",
    author="Vert Capital",
    author_email="thiago@vert-capital.com",
    classifiers=[],
    install_requires=[
        "boto3>=1.17.88",
        "requests",
        "pytz",
    ],
)
