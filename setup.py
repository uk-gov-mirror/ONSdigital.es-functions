from setuptools import find_packages, setup

requirements = [
    "boto3",
    "immutables",
    "pandas",
    "spp-logger @ git+https://github.com/ONSdigital/spp-logger"
]

setup(
    name='es_aws_functions',
    version='1.0',
    packages=find_packages(),
    install_requires=requirements
 )
