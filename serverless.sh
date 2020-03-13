#!/usr/bin/env bash

# Serverless deployment
cd functions-deploy-repository
mkdir layer
mkdir layer/python
cp -R es_aws_functions layer/python/es_aws_functions

python3 -m site
ls
apt-get install python3 -y

ls /usr/lib/python3/dist-packages/
ls /usr/lib/python3.7
ls /usr/local/lib/python3.7/dist-packages


ls /usr/local/lib/python3.7
ls /usr/local/lib/python3.7/site-packages
cp -r /usr/local/lib/python3.7/site-packages pythonlayer
cd pythonlayer
mv site-packages/ python/
cd ..

echo Deploying to AWS...
serverless deploy --verbose;
rm -rf layer/
