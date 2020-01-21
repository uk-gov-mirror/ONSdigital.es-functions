#!/usr/bin/env bash

cd aws-functions-repository
echo Destroying serverless bundle...
serverless remove --verbose;
