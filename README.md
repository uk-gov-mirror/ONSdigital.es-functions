
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
This project can be automatically deployed via docker and serverless framework. To do so, follow:<br>
```
./do.sh build
aws-vault exec serverless -- ./do.sh deploy
```
You will need the correct credentials stored in aws vault so that this works.

[Back to top](#top)
<hr>
