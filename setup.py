from setuptools import find_packages, setup

setup(name='es_aws_functions',
      version='1.0',
      packages=find_packages(), install_requires=['boto3', 'botocore', 'pandas']
      )
