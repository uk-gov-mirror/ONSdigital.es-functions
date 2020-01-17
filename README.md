
# es_aws_functions <a name='top'>
Common functions used by the econstats results processes.
<br>
Once layer is attached to lambda, the package can be used as follows:
```
from es_aws_functions import aws_functions
data = aws_functions.read_from_s3("MyBucketName", "MyFileName")
```
<hr>
  
### Contents:
##### Exception Classes
[Method Failure](#methodfailure)<br>
[No Data In Queue Error](#nodatainqueue)<br>
[Do Not Have All Data Error](#donthavealldata)<br>

[AWS Functions](AWSFunctions.md)<br>
[Test Generic Library](TestGenericLibrary.md)<br>

##### General Functions
[Calculate Adjacent Periods](#calculateadjacentperiods)<br>

##### Other
[Automated Deployment](#autodeploy)<br>
<hr>

## Exception_Classes

### Class DoNotHaveAllDataError  <a name='donthavealldata'>
Custom exception used by the modules which need to take more than one message from a queue, but fail to.

[Back to top](#top)
<hr>

### Class MethodFailure  <a name='methodfailure'>
Custom exception thrown when the method has encountered an exception.
  
#### Parameters:
It expects to be passed the error message from the method.

#### Usage:
```
if str(type(json_response)) != "<class 'str'>":
    raise exception_classes.MethodFailure(json_response['error'])
```

```
except exception_classes.MethodFailure as e:
    error_message = e.error_message
    log_message = "Error in " + method_name + "."
```
  
[Back to top](#top)
<hr>

### Class NoDataInQueueError  <a name='nodatainqueue'>
Custom exception thrown when response does not contain any messages.
  
[Back to top](#top)
<hr>



## General Functions
### Calculate Adjacent Periods <a name='calculateadjacentperiods'>
This function takes a period (Format: YYYYMM) and a periodicity. <br>

#### Parameters:
Period: Format YYYYMM of the period you are calculating for. - Type: String/Int. <br>
Periodicity: '01' Monthly, '02' Annually, '03' Quarterly - Type: String. <br>

#### Return:
Period: Format YYYYMM of the previous period. Type: String. <br>

#### Usage:
```
general_function.calculate_adjacent_periods("201606", "03")
```

[Back to top](#top)
<hr>



## Other
### Automated Deployment <a name='autodeploy'>
This project can be automatically deployed via docker and serverless framework. To do so, follow:<br>
```
./do.sh build
aws-vault exec serverless -- ./do.sh deploy
```
You will need the correct credentials stored in aws vault so that this works.

[Back to top](#top)
<hr>
