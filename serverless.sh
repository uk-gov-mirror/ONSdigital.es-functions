#!/usr/bin/env bash

# Serverless deployment
cd functions-deploy-repository
mkdir layer
mkdir layer/python
cp -R es_aws_functions layer/python/es_aws_functions


whereis python3.7/pandas
whereis python3.7



python3 -m pandas
ls -R /usr/local/bin/python

cp -r /usr/local/lib/python3.7/site-packages pythonlayer
cd pythonlayer
mv site-packages/ python/
cd ..

echo Deploying to AWS...
serverless deploy --verbose;
rm -rf layer/
