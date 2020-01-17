
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
##### AWS Functions
[Delete Data](#deletedata)<br>
[Get Data](#getdata)<br>
[Get DataFrame](#getdataframe)<br>
[Get SQS Message](#getsqsmessage)<br>
[Get SQS Messages](#getsqsmessages)<br>
[Read DataFrame From S3](#readdataframefroms3)<br>
[Read From S3](#readfroms3)<br>
[Save Data](#savedata)<br>
[Save To S3](#savetos3)<br>
[Send SNS Message](#sendsnsmessage)<br>
[Send SNS Message With Anomalies](#sendsnsmessageanomalies)<br>
[Send SQS Message](#sendsqsmessage)<br>
[Write Dataframe To CSV](#savetocsv)<br>
##### General Functions
[Calculate Adjacent Periods](#calculateadjacentperiods)<br>
##### Test Generic Library
[Client Error](#clienterror)<br>
[Create Bucket](#createbucket)<br>
[Create Client](#createclient)<br>
[General Error](#generalerror)<br>
[Incomplete Read Error](#incompletereaderror)<br>
[Key Error](#keyerror)<br>
[Method Error](#methoderror)<br>
[Replacement Get Dataframe](#replacementgetdataframe)<br>
[Replacement Save Data](#replacementsavedata)<br>
[Upload Files](#uploadfiles)<br>
[Value Error](#valueerror)<br>
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

## AWS_Functions

### Delete From S3 <a name='deletedata'>
Given the name of the bucket and the filename(key), this function will
delete a file in any format. Performs check if file exists, else return
error.

#### Parameters:
bucket_name: Name of the S3 bucket - Type: String <br>
file_name: Name of the file - Type: String

#### Return:
Success or error message - Type: String

#### Usage:
```
# Stored in variable to retrieve returned success/error message,
# to be passed to the logger.
delete = aws_functions.delete_data(bucket_name, file_name)
```
[Back to top](#top)
<hr>

### Get Data <a name='getdata'>
Get data function recieves a message from an sqs queue, extracts the bucket and filename, then uses them to get the file from s3. If no messages are in the queue, or if the message does not come from the preceding module, the bucket_name and key given as parameters are used instead.
<br><br>
SQS only supports message length of 256k, so this function is to be used instead of get_sqs_message when the data size approaches this figure. Used in conjunction with save_data.<br><br>

Data is returned as a json string. To use as dataframe you will need to json.loads and pd.dataframe() the response.

#### Parameters: 
queue_url: The url of the queue to retrieve message from - Type: String<br>
bucket_name: The default bucket name to use if no message from previous module - Type: String<br>
key: The default file name to use if no message from the previous module - Type: String<br>
incoming_message_group: The name of the message group from previous module - Type: String (example: enrichmentOut)<br>

#### Returns:
data: The data from s3 - Type: Json<br>
receipt_handle: The receipt_handle of the incoming message(used to delete old message) - Type: String

#### Usage:
```
message_json, receipt_handle = aws_functions.get_data(queue_url, bucket_name, "enrichment_out.json",incoming_message_group)
```
[Back to top](#top)
<hr>

### Get DataFrame <a name='getdataframe'>
Get data function recieves a message from an sqs queue, extracts the bucket and filename, then uses them to get the file from s3. If no messages are in the queue, or if the message does not come from the preceding module, the bucket_name and key given as parameters are used instead.
<br><br>
SQS only supports message length of 256k, so this function is to be used instead of get_sqs_message when the data size approaches this figure. Used in conjunction with save_data.<br><br>

Data is returned as a DataFrame.

#### Parameters: 
queue_url: The url of the queue to retrieve message from - Type: String<br>
bucket_name: The default bucket name to use if no message from previous module - Type: String<br>
key: The default file name to use if no message from the previous module - Type: String<br>
incoming_message_group: The name of the message group from previous module - Type: String (example: enrichmentOut)<br>

#### Returns:
data: The data from s3 - Type: DataFrame<br>
receipt_handle: The receipt_handle of the incoming message(used to delete old message) - Type: String

#### Usage:
```
output_Dataframe, receipt_handle = aws_functions.get_dataframe(queue_url, bucket_name, "enrichment_out.json",incoming_message_group)
```
[Back to top](#top)
<hr>

### Get SQS Message <a name='getsqsmessage'>
This method retrieves the data from the specified SQS queue. <br><br>There is a requirement from the combiner module for the ability to retrieve up to 3 messages from the queue. If such capability is needed, then include the number as the second parameter. There is no need if you only require one message because of a default.

#### Parameters: 
queue_url: The url of the SQS queue.<br>
max_number_of_messages: Number of messages to pick up from queue(default 1) - Type: Int

#### Returns:
Messages from queue - Type: json string

#### Usage:
```
response = aws_functions.get_sqs_message(queue_url)
-------
or
-------
responses = aws_functions.get_sqs_message(queue_url, 3)
```
[Back to top](#top)
<hr>

### Get SQS Messages <a name='getsqsmessages'>
This method retrieves a number of messages from the sqs queue.
It takes 10 messages from the queue, then checks each to see if it comes from
the appropriate message_group.

#### Parameters: 
queue_url: The url of the SQS queue.<br>
number_of_messages: Number of messages expected(will raise error if not met) - Type: Int
incoming_message_group: The message group of messages to collect.

#### Returns:
Messages from queue - List of Json Strings

#### Usage:
```
response = aws_functions.get_sqs_messages(queue_url, 3, 'aggregation')
```

[Back to top](#top)
<hr>

### Read DataFrame From S3 <a name='readdataframefroms3'>
Given the name of the bucket and the filename(key), this function will
return contents of a file. File is Dataframe format.

#### Parameters:
bucket_name: Name of the S3 bucket - Type: String <br>
file_name: Name of the file - Type: String

#### Return:
input_file: The JSON file in S3 - Type: String

#### Usage:
```
data_dataframe = aws_functions.read_dataframe_from_s3(bucket_name, file_name)
```
[Back to top](#top)
<hr>

### Read From S3 <a name='readfroms3'>
Given the name of the bucket and the filename(key), this function will
return a file. File is JSON format.

#### Parameters:
bucket_name: Name of the S3 bucket - Type: String <br>
file_name: Name of the file - Type: String

#### Return:
input_file: The JSON file in S3 - Type: String

#### Usage:
```
data = aws_functions.read_from_s3(bucket_name, file_name)
#Note that this function returns the data as a string. To use further might require below steps
message_json = json.loads(data)
message_dataframe = pd.DataFrame(message_json)
```
[Back to top](#top)
<hr>

### Save Data <a name='savedata'>
Save data function stores data in s3 and passes the bucket & filename onto sqs queue. SQS only supports message length of 256k, so this function is to be used instead of send_sqs_message when the data size approaches this figure. Used in conjunction with get_data.

#### Parameters:
bucket_name: The name of the s3 bucket to use to save data - Type: String<br>
file_name: The name to give the file being saved - Type: String<br>
data: The data to be saved - Type Json string<br>
queue_url: The url of the queue to use in sending the file details - Type: String<br>
message_id: The label of the message sent to sqs(Message_group_id, what module sent the message) - Type: String (example: enrichmentOut)<br>

#### Return:
Nothing

#### Usage:
```
final_output = json.loads(json_response)
aws_functions.save_data(bucket_name, file_name, str(final_output), queue_url, sqs_messageid_name)
```

[Back to top](#top)
<hr>

### Save To S3 <a name='savetos3'>
This function uploads a specified set of data to the s3 bucket under the given name.<br>

#### Parameters:
bucket_name: Name of the bucket you wish to upload too - Type: String.<br>
output_file_name: Name you want the file to be called on s3 - Type: String.<br>
output_data: The data that you wish to upload to s3 - Type: JSON string. - Note, this must be string<br>

#### Return:
Nothing

#### Usage:
```
aws_functions.save_to_s3(bucket_name, file_name, data)
```
[Back to top](#top)
<hr>

### Send SNS Message <a name='sendsnsmessage'>
This method is responsible for sending a notification to the specified arn, so that it can be used to relay information for the BPM to use and handle.

#### Parameters:
checkpoint: The current checkpoint location - Type: String.<br>
sns_topic_arn: The arn of the sns topic you are directing the message at - Type: String.<br>
module_name: The name of the module currently being run - Type: String.<br>

#### Return:
Json string containing metadata about the message.

#### Usage:
```
aws_functions.send_sns_message(checkpoint, arn, "Strata")
```
[Back to top](#top)
<hr>

### Send SNS Message With Anomalies <a name='sendsnsmessageanomalies'>
This method is responsible for sending a notification to the specified arn, so that it can be used to relay information for the BPM to use and handle.<br><br>
This version of the send to sns is used by modules that also send a report of data anomalies

#### Parameters:
checkpoint: The current checkpoint location - Type: String.<br>
anomalies: Json formatted summary of data anomalies - Type: String<br>
module_name: The name of the module currently being run - Type: String.<br>
sns_topic_arn: The arn of the sns topic you are directing the message at - Type: String.<br>

#### Return:
Nothing

#### Usage:
```
aws_functions.send_sns_message_with_anomalies(checkpoint, anomalies, arn, "Enrichment")
```
[Back to top](#top)
<hr>

### Send SQS Message <a name='sendsqsmessage'>
This method is responsible for sending data to an SQS queue.

#### Parameters: 
queue_url: The url of the SQS queue. - Type: String<br>
message: The message/data you wish to send to the SQS queue - Type: String<br>
output_message_id: The label of the record in the SQS queue - Type: String<br>

#### Return:
Json string containing metadata about the message.

#### Usage:
```
# Use as part of save data
sqs_message = json.dumps({"bucket": bucket_name, "key": file_name})
aws_functions.send_sqs_message(queue_url, sqs_message, message_id)
----------------------
json_response = returned_data.get('Payload').read().decode("UTF-8")
aws_functions.send_sqs_message(queue_url, json_response, "Strata")

```
[Back to top](#top)
<hr>

### Write DataFrame To CSV <a name='savetocsv'>
This function takes a Dataframe and stores it in a specific bucket.<br>

#### Parameters:
Dataframe: The Dataframe you wish to save - Type: Dataframe.<br>
Bucket_name: Name of the bucket you wish to save the csv into - Type: String.<br>
Output_data: Filename: The name given to the CSV - Type: String.<br>

#### Return:
Nothing

#### Usage:
```
aws_functions.write_dataframe_to_csv(dataframe, bucket_name, filename)
```
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
general_function.calculate_adjactent_periods("201606", "03")
```

[Back to top](#top)
<hr>

## Test Generic Library
### Client Error <a name='clienterror'>
#### Parameters:
#### Return:
#### Usage:
```
test_generic_library.client_error()
```

[Back to top](#top)
<hr>

### Create Bucket <a name='createbucket'>
#### Parameters:
#### Return:
#### Usage:
```
test_generic_library.create_bucket("test_bucket")
```

[Back to top](#top)
<hr>

### Create Client <a name='createclient'>
#### Parameters:
#### Return:
#### Usage:
```
test_generic_library.create_client("s3", "eu-west-2")
```

[Back to top](#top)
<hr>

### General Error <a name='generalerror'>
#### Parameters:
#### Return:
#### Usage:
```
test_generic_library.general_error()
```

[Back to top](#top)
<hr>

### Incomplete Read Error <a name='incompletereaderror'>
#### Parameters:
#### Return:
#### Usage:
```
test_generic_library.incomplete_read_error()
```

[Back to top](#top)
<hr>

### Key Error <a name='keyerror'>
#### Parameters:
#### Return:
#### Usage:
```
test_generic_library.key_error()
```

[Back to top](#top)
<hr>

### Method Error <a name='methoderror'>
#### Parameters:
#### Return:
#### Usage:
```
test_generic_library.method_error()
```

[Back to top](#top)
<hr>

### Replacement Get Dataframe <a name='replacementgetdataframe'>
#### Parameters:
#### Return:
#### Usage:
```
test_generic_library.replacement_get_dataframe("", "test_bucket", "file_1.json", "")
```

[Back to top](#top)
<hr>

### Replacement Save Data <a name='replacementsavedata'>
#### Parameters:
#### Return:
#### Usage:
```
test_generic_library.replacement_save_data("", "file_1.json", '{"key": "value"}'}, "", "")
```

[Back to top](#top)
<hr>

### Upload Files <a name='uploadfiles'>
#### Parameters:
#### Return:
#### Usage:
```
test_generic_library.upload_files(client, "test_bucket", ["file_1.json", "file_2.json"])
```

[Back to top](#top)
<hr>

### Value Error <a name='valueerror'>
#### Parameters:
#### Return:
#### Usage:
```
test_generic_library.value_error()
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
