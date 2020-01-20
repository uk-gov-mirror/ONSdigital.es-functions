# Exception Classes <a name='top'>
[Back](README.md)
## Contents
[Method Failure](#methodfailure)<br>
[No Data In Queue Error](#nodatainqueue)<br>
[Do Not Have All Data Error](#donthavealldata)<br>
## Functions
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
