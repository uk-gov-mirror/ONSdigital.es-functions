# es-aws-functions <a name='top'>
Common functions used by the econstats results process.
<br>
Once layer is attached to lambda, the package can be used as follows:
```
from esawsfunctions import funk
data = funk.read_from_s3("MyBucketName", "MyFileName")
```
<br>
### Contents:
[No data in queue error](#nodatainqueue)<br>
[Read from s3](#readfroms3)<br>
[Read dataframe from s3](#readdataframefroms3)<br>
[Save to s3](#savetos3)<br>
[Send sqs message](#sendsqsmessage)<br>
[Send sns message](#sendsnsmessage)<br>
[Send sns message with anomalies](#sendsnmessageanomalies)<br>
[Get sqs message](#getsqsmessage)<br>
[Save Data](#savedata)<br>
[Get Data](#getdata)<br>
<br>
## Class NoDataInQueueError  <a name='nodatainqueue'>
Custom exception thrown when response does not contain any messages.
[Back to top](#top)
<hr>
## Read From s3 <a name='readfroms3'>
Given the name of the bucket and the filename(key), this function will
return a file. File is JSON format.

### Parameters:
bucket_name: Name of the S3 bucket - Type: String <br>
file_name: Name of the file - Type: String

### Return:
input_file: The JSON file in S3 - Type: String

### Usage:
```
data = funk.read_from_s3("MyBucketName", "MyFileName")
message_json = json.loads(message_json)
message_dataframe = pd.DataFrame(message_json)
```
[Back to top](#top)
<hr>
## Read Dataframe from s3 <a name='readdataframefroms3'>
Given the name of the bucket and the filename(key), this function will
return contents of a file. File is Dataframe format.

### Parameters:
bucket_name: Name of the S3 bucket - Type: String <br>
file_name: Name of the file - Type: String

### Return:
input_file: The JSON file in S3 - Type: String

### Usage:
```
data_dataframe = funk.read_dataframe_from_s3("MyBucketName", "MyFileName")
```
[Back to top](#top)
<hr>
## Save to s3 <a name='savetos3'>
This function uploads a specified set of data to the s3 bucket under the given name.<br>

### Parameters:
bucket_name: Name of the bucket you wish to upload too - Type: String.<br>
output_file_name: Name you want the file to be called on s3 - Type: String.<br>
output_data: The data that you wish to upload to s3 - Type: JSON string. - Note, this must be string<br>

### Return:
Nothing

### Usage:
```
funk.save_to_s3(bucket_name, file_name, data)
```
[Back to top](#top)
<hr>
## Send sqs message <a name='sendsqsmessage'>
This method is responsible for sending data to an SQS queue.

### Parameters: 
queue_url: The url of the SQS queue. - Type: String<br>
message: The message/data you wish to send to the SQS queue - Type: String<br>
output_message_id: The label of the record in the SQS queue - Type: String<br>

### Return:
Json string containing metadata about the message.

### Usage:
```
# Use as part of save data
sqs_message = json.dumps({"bucket": bucket_name, "key": file_name})
funk.send_sqs_message(queue_url, sqs_message, message_id)
----------------------
json_response = returned_data.get('Payload').read().decode("UTF-8")
funk.send_sqs_message(queue_url, json_response, "Strata")

```
[Back to top](#top)
<hr>
## Send sns message <a name='sendsnsmessage'>
This method is responsible for sending a notification to the specified arn, so that it can be used to relay information for the BPM to use and handle.

### Parameters:
checkpoint: The current checkpoint location - Type: String.<br>
module_name: The name of the module currently being run - Type: String.<br>
sns_topic_arn: The arn of the sns topic you are directing the message at - Type: String.<br>

### Return:
Json string containing metadata about the message.

### Usage:
```
funk.send_sns_message(checkpoint, arn, "Strata")
```
[Back to top](#top)
<hr>
## Send sns message with anomalies <a name='sendsnmessageanomalies'>
This method is responsible for sending a notification to the specified arn, so that it can be used to relay information for the BPM to use and handle.<br><br>
This version of the send to sns is used by modules that also send a report of data anomalies

### Parameters:
checkpoint: The current checkpoint location - Type: String.<br>
anomalies: Json formatted summary of data anomalies - Type: String<br>
module_name: The name of the module currently being run - Type: String.<br>
sns_topic_arn: The arn of the sns topic you are directing the message at - Type: String.<br>

### Return:
Nothing

### Usage:
```
funk.send_sns_message_with_anomalies(checkpoint, anomalies, arn, "Enrichment")
```
[Back to top](#top)
<hr>
## Get sqs message <a name='getsqsmessage'>
This method retrieves the data from the specified SQS queue.

### Parameters: 
queue_url: The url of the SQS queue.

### Returns:
Messages from queue - Type: json string

### Usage:
```
response = funk.get_sqs_message(queue_url)
```
[Back to top](#top)
<hr>
### Save Data <a name='savedata'>
Save data function stores data in s3 and passes the bucket & filename onto sqs queue. SQS only supports message length of 256k, so this function is to be used instead of send_sqs_message when the data size approaches this figure. Used in conjunction with get_data.

### Parameters:
bucket_name: The name of the s3 bucket to use to save data - Type: String<br>
file_name: The name to give the file being saved - Type: String<br>
data: The data to be saved - Type Json string<br>
queue_url: The url of the queue to use in sending the file details - Type: String<br>
message_id: The label of the message sent to sqs(Message_group_id, what module sent the message) - Type: String<br>

### Return:
Nothing

### Usage:
```
final_output = json.loads(json_response)
funk.save_data(bucket_name, file_name, str(final_output), queue_url, sqs_messageid_name)
```
[Back to top](#top)
<hr>
### Get Data <a name='getdata'>
Get data function recieves a message from an sqs queue, extracts the bucket and filename, then uses them to get the file from s3. If no messages are in the queue, or if the message does not come from the preceding module, the bucket_name and key given as parameters are used instead.
<br><br>
SQS only supports message length of 256k, so this function is to be used instead of get_sqs_message when the data size approaches this figure. Used in conjunction with save_data.<br><br>

Data is returned as a json string. To use as dataframe you will need to json.loads and pd.dataframe() the response.

### Parameters: 
queue_url: The url of the queue to retrieve message from - Type: String
bucket_name: The default bucket name to use if no message from previous module - Type: String
key: The default file name to use if no message from the previous module - Type: String
incoming_message_group: The name of the message group from previous module - Type: String

### Returns:
data: The data from s3 - Type: Json
receipt_handle: The receipt_handle of the incoming message(used to delete old message) - Type: String

### Usage:
```
message_json, receipt_handle = funk.get_data(queue_url, bucket_name, "enrichment_out.json",incoming_message_group)
```
<hr>
[Back to top](#top)
