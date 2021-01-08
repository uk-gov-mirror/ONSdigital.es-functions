from setuptools import find_packages, setup

with open("./requirements.txt") as f:
    dev_reqs = f.read()

setup(name='es_aws_functions',
      version='1.0',
      packages=find_packages(), install_requires=dev_reqs
      )
