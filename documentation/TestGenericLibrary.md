# Test Generic Library <a name='top'>
[Back](../README.md)
## Contents
### Assertions
[Method Assert](#methodassert)<br>
[Wrangler Assert](#wranglerassert)<br><br>

### Functions
[Client Error](#clienterror)<br>
[Create Bucket](#createbucket)<br>
[Create Client](#createclient)<br>
[General Error](#generalerror)<br>
[Incomplete Read Error](#incompletereaderror)<br>
[Key Error](#keyerror)<br>
[Replacement Get Dataframe](#replacementgetdataframe)<br>
[Replacement Invoke](#replacementinvoke)<br>
[Replacement Save Data](#replacementsavedata)<br>
[Replacement Save To S3](#replacementsavetos3)<br>
[Upload Files](#uploadfiles)<br>
[Value Error](#valueerror)<br>
[Wrangler Method Error](#methoderror)<br>


## Assertions
Because the wrangler and method behave differently in sad path, we have to use different types of assertion to ensure they behave correctly. To do this, we pass a specific assertion into the generic methods.

### Method Assert <a name='methodassert'>
Function to perform sad path assertion on methods<br>
    (method sad path is different to wrangler)<br>
Runs function to get output, then checks output.

#### Parameters:
lambda_function: Lambda function to test - Type: Function<br>
runtime_variables: Runtime variables to send to function - Type: Dict<br>
expected_message: The error message that is expected from the test - Type: String

#### Return
Test Pass/Fail

#### Usage
```
# Passed in to test:
test_generic_library.client_error(which_lambda, which_runtime_variables,
                                      which_environment_variables, which_data,
                                      expected_message, assertion)
------
# Within test:
assertion(lambda_function, runtime_variables, expected_message)

```
[Back to top](#top)
<hr>

### Wrangler Assert <a name='wranglerassert'>
Function to perform sad path assertion on wrangler<br>
    (method sad path is different to wrangler)<br>
    Runs function and asserts that exception is raised, then checks the contents.
#### Parameters:
lambda_function: Lambda function to test - Type: Function<br>
runtime_variables: Runtime variables to send to function - Type: Dict<br>
expected_message: The error message that is expected from the test - Type: String

#### Return
Test Pass/Fail

#### Usage
```
# Passed in to test:
test_generic_library.client_error(which_lambda, which_runtime_variables,
                                      which_environment_variables, which_data,
                                      expected_message, assertion)
------
# Within test:
assertion(lambda_function, runtime_variables, expected_message)

```
[Back to top](#top)
<hr>

## Functions

### Client Error <a name='clienterror'>
Function to trigger a client error in a lambda. By not mocking any of the boto3 functions, once any are used in code they will trigger client error due to lack of credentials.<br><br>

If used on a method, data is part of the runtime_variables, so the file_name is loaded in
and the file added to the runtime_variables dictionary.

#### Parameters:
lambda_function: Lambda function to test - Type: Function<br>
runtime_variables: Runtime variables to send to function - Type: Dict<br>
environment_variables: Environment Vars to send to function - Type: Dict<br>
file_name: Name of file to retrieve data from - Type: String<br>
expected_message: The error message that is expected from the test - Type: String<br>
assertion: Type of assertion to use - Type: Function

#### Return: 
Test Pass/Fail<br>
#### Usage:
```
test_generic_library.client_error(which_lambda, which_runtime_variables, which_environment_variables, which_data, expected_message, assertion)
```

[Back to top](#top)
<hr>

### Create Bucket <a name='createbucket'>
Create an s3 bucket.<br>
  
#### Parameters:
bucket_name: Name of bucket to create - Type: String<br>

#### Return:
client: S3 client that created bucket - Type: Boto3 Client<br>

#### Usage:
```
client = test_generic_library.create_bucket(bucket_name)
```

[Back to top](#top)
<hr>

### Create Client <a name='createclient'>
Create a boto3 client for use with aws tests.<br>

#### Parameters:
client_type: Type of client(eg. s3, lambda, sqs etc) - Type: String<br>
region: Region to create client in(default is eu-west-2) - Type: String

#### Return:
client: Requested boto3 client - Type: Boto3 Client

#### Usage:
```
client = test_generic_library.create_client("s3")
----
or
----
client = test_generic_library.create_client("s3", "eu-west-1")
```

[Back to top](#top)
<hr>

### General Error <a name='generalerror'>
Function to trigger a general error in a given lambda.<br><br>

The variable 'mockable_function' defines the function in the lambda that will
be mocked out. This should be something fairly early in the code (but still
within try/except). e.g. "enrichment_wrangler.EnvironSchema"

#### Parameters:
lambda_function: Lambda function to test - Type: Function<br>
runtime_variables: Runtime variables to send to function - Type: Dict<br>
environment_variables: Environment Vars to send to function - Type: Dict<br>
mockable_function: The function in the code to mock out (and attach side effect to) - Type: String<br>
expected_message: The error message that is expected from the test - Type: String<br>
assertion: Type of assertion to use - Type: Function

#### Return:
Test Pass/Fail

#### Usage:
```
test_generic_library.general_error(which_lambda, which_runtime_variables, which_environment_variables, mockable_function, expected_message, assertion)
```

[Back to top](#top)
<hr>

### Incomplete Read Error <a name='incompletereaderror'>
Function to trigger an incomplete read error in a given wrangler.

Takes in a valid file(s) so that the function performs until after the lambda invoke.

#### Parameters:
lambda_function: Lambda function to test - Type: Function<br>
runtime_variables: Runtime variables to send to function - Type: Dict<br>
environment_variables: Environment Vars to send to function - Type: Dict<br>
file_list: List of input files for the function - Type: List<br>
wrangler_name: Wrangler that is being tested, used in mocking boto3. - Type: String

#### Return:
Test Pass/Fail

#### Usage:
  
```
test_generic_library.incomplete_read_error(lambda_wrangler_function,
                                                   wrangler_runtime_variables,
                                                   wrangler_environment_variables,
                                                   file_list,
                                                   "enrichment_wrangler")
```

[Back to top](#top)
<hr>

### Key Error <a name='keyerror'>
Function to trigger a key error in a given lambda.<br><bR>

Makes use of an empty dict of runtime variables,<br>
which triggers a key error once access is attempted.

#### Parameters:
lambda_function: Lambda function to test - Type: Function<br>
environment_variables: Environment Vars to send to function - Type: Dict<br>
expected_message: The error message that is expected from the test - Type: String<br>
assertion: Type of assertion to use - Type: Function<br>
runtime_variables: Runtime variables to send to function(default is empty dict) - Type: Dict

#### Return:
Test Pass/Fail

#### Usage:
```
test_generic_library.key_error(which_lambda, expected_message, assertion, which_environment_variables)
```

[Back to top](#top)
<hr>


### Replacement Get Dataframe <a name='replacementgetdataframe'>
Function to replace the aws-functions.get_dataframe when performing tests.<br><Br>

Instead of getting an sqs message and then using it to define the file to get,
Goes straight to s3 for the data. Variables marked as 'Unused' are variables that the
original function needed but the replacement one doesn't.<br><br>

Takes the same parameters as get_dataframe, but only uses file_name and data.
#### Parameters:
sqs_queue_url: Name of sqs queue. Unused<br>
bucket_name: Name of bucket to retrieve data from - Type: String<br>
in_file_name: Name of file to read in - Type: String<br>
incoming_message_group: Name of message group. Unused
    
#### Return:
data: Data from file - Type: Dataframe
receipt: Int to simulate message receipt (999)- Type: Int

#### Usage:
```
test_generic_library.replacement_get_dataframe("", "test_bucket", "file_1.json", "")
```

[Back to top](#top)
<hr>

### Replacement Invoke <a name='replacementinvoke'>
Function to replace the lambda invoke, it instead saves data to be compared.<br><br>

Takes the same parameters as get_dataframe, but only uses file_name and data.<br><br>

#### Parameters
FunctionName: Name of the lambda to be invoked. Unused<br>
Payload: The passed in parameters and data for the original invoke.

#### Return
-

#### Usage:
```
test_generic_library.replacement_invoke("", json_dumps({"data": "", "column_name": "", ...}))
```

[Back to top](#top)
<hr>

### Replacement Save Data <a name='replacementsavedata'> 
Function to replace the aws-functions.save_data when performing tests.<br><br>

Saves a copy of the file locally.<br><br>

Takes the same parameters as save_data, but only uses file_name and data.
#### Parameters:
bucket_name: Name of bucket. Unused.<br>
file_name: Name of file to save in tests/fixtures - Type: String<br>
data: Data to save - Type: Json String<br>
sqs_queue_url: Name of sqs queue. Unused<br>
sqs_message_id: Name of message group. Unused<br>
run_id: ID to identify the run. Unused

#### Return:
-

#### Usage:
```
test_generic_library.replacement_save_data("", "file_1.json", '{"key": "value"}'}, "", "", "")
```

[Back to top](#top)
<hr>

### Replacement Save To S3 <a name='replacementsavetos3'> 
Function to replace the aws-functions.save_data when performing tests.<br><br>

Saves a copy of the file locally.<br><br>

Takes the same parameters as save_data, but only uses file_name and data.
#### Parameters:
bucket_name: Name of bucket. Unused.<br>
file_name: Name of file to save in tests/fixtures - Type: String<br>
data: Data to save - Type: Json String<br>
run_id: ID to identify the run. Unused

#### Return:
-

#### Usage:
```
test_generic_library.replacement_save_to_s3("", "file_1.json", '{"key": "value"}'}, "")
```

[Back to top](#top)
<hr>

### Upload Files <a name='uploadfiles'>
Upload a list of files to a given s3 bucket from the test/fixtures folder.<br>
Key of the uploaded file(s) is their filename.
  
#### Parameters:
client: S3 Client - Type: Boto3 Client<br>
bucket_name: Name of bucket to place files in - Type: String<br>
file_list: List of files to upload - Type: List

#### Return:
client: S3 client that uploaded files

#### Usage:
```
test_generic_library.upload_files(client, "test_bucket", ["file_1.json", "file_2.json"])
```

[Back to top](#top)
<hr>

### Value Error <a name='valueerror'>
Function to trigger a value error in a given function.<br><br>

Does so by passing an empty list of environment variables
to trigger an error with marshmallow.


#### Parameters:
lambda_function: Lambda function to test - Type: Function<br>
expected_message: The error message that is expected from the test - Type: String<br>
assertion: Type of assertion to use - Type: Function<br>
runtime_variables: Runtime variables to send to function - Type: Dict<br>
environment_variables: Environment Vars to send to function - Type: Dict

#### Return:
Test Pass/Fail

#### Usage:
```
test_generic_library.value_error(which_lambda, expected_message, assertion)
```

[Back to top](#top)
<hr>

### Wrangler Method Error <a name='methoderror'>
Function to trigger a method error in a given function.<br><Br>

Takes in a valid file(s) so that the function performs until after the lambda invoke.

#### Parameters:
lambda_function: Lambda function to test - Type: Function<br>
runtime_variables: Runtime variables to send to function - Type: Dict<br>
environment_variables: Environment Vars to send to function - Type: Dict<br>
file_list: List of input files for the function - Type: List<br>
wrangler_name: Wrangler that is being tested, used in mocking boto3. - Type: String

#### Return:
Test Pass/Fail

#### Usage:
```
test_generic_library.wrangler_method_error(lambda_wrangler_function,
                                          wrangler_runtime_variables,
                                          wrangler_environment_variables,
                                          file_list,
                                          "enrichment_wrangler")
```

[Back to top](#top)
<hr>