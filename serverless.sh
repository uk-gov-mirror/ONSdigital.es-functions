#!/usr/bin/env bash

# Serverless deployment
cd functions-deploy-repository
mkdir layer
mkdir layer/python
cp -R es_aws_functions layer/python/es_aws_functions

ls -R -l /usr/local/bin/
ls -R -l /usr/local/bin/python3.7
ls -R -l /usr/bin
cp -r /usr/local/lib/python3.7/site-packages pythonlayer
cd pythonlayer
mv site-packages/ python/
cd ..

echo Deploying to AWS...
serverless deploy --verbose;
rm -rf layer/
