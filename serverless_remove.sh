#!/usr/bin/env bash

cd functions-repository
echo Destroying serverless bundle...
serverless remove --verbose;
