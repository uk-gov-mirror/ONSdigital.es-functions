
# es_aws_functions <a name='top'>
Common functions used by the econstats results processes.
<br>
Once layer is attached to lambda, the package can be used as follows:
```
from es_aws_functions import aws_functions
data = aws_functions.read_from_s3("MyBucketName", "MyFileName")
```
<hr>
  
## Module Contents:
[AWS Functions](AWSFunctions.md)<br>
[Exception Classes](ExceptionClasses.md)<br>
[General Functions](GeneralFunctions.md)<br>
[Test Generic Library](TestGenericLibrary.md)<br>
[Test Module Example](TestModuleExample.md)

## Automated Deployment <a name='autodeploy'>

Concourse should auto-deploy the layer, if you wish to do it manually and deploy via docker and serverless framework. To do so, follow:<br>
```
./do.sh build
aws-vault exec serverless -- ./do.sh deploy
```
You will need the correct credentials stored in aws vault so that this works.

## Python Layer

In addition to the aws-functions layer that contains our own library. We make use of a python layer to hold various dependencies in our lambdas.
<br>
This is up to automatically download and package the dependencies and versions held in the layer-requirements.txt file.
<br>
Deployment is handled in the same way. Any changes to dependencies should go into layer-requirements file to be picked up the the next deployment.

[Back to top](#top)
<hr>
