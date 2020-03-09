#!/usr/bin/env bash

# Serverless deployment
cd functions-deploy-repository
mkdir layer
mkdir layer/python
cp -R es_functions layer/python/es_functions
echo Deploying to AWS...
serverless deploy --verbose;
rm -rf layer/
