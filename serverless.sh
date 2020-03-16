#!/usr/bin/env bash

# Serverless deployment
cd functions-deploy-repository
mkdir layer
mkdir layer/python
cp -R es_aws_functions layer/python/es_aws_functions
mkdir pythonlayer

ls /
ls /site-packages
#cp -r /usr/local/lib/python3.7/site-packages/ pythonlayer/site-packages
cp -r /site-packages pythonlayer/site-packages

cd pythonlayer
ls
du site-packages
mv site-packages/ python/
du -c -h python
ls
zip python.zip python/
cd ..

echo Deploying to AWS...
serverless deploy --verbose;
rm -rf layer/
