#!/usr/bin/env bash

# Serverless deployment
cd functions-deploy-repository
mkdir layer
mkdir layer/python
cp -R es_aws_functions layer/python/es_aws_functions
mkdir pythonlayer

find / -name "site-packages"
cp -r /usr/local/lib/python3.7/site-packages/ pythonlayer/site-packages
ls
cd pythonlayer
ls
mv site-packages/ python/
zip python.zip python/
cd ..

echo Deploying to AWS...
serverless deploy --verbose;
rm -rf layer/
