import json
import random
from io import StringIO

import boto3
import pandas as pd
from botocore.exceptions import ClientError

from es_aws_functions import exception_classes

extension_types = {
    ".json": "application/json",
    ".csv": "text/plain"
}


def delete_data(bucket_name, file_name, file_prefix="", file_extension=".json"):
    """
    Deletes specified file from specified S3 bucket.
    Checks if file exists before deletion.
    If file does not exist, return error message.

    :param bucket_name: The name of the bucket containing the file - Type: String
    :param file_name: The name of the file being deleted - Type: String
    :param file_prefix: Optional, run id to be added as file name prefix - Type: String
    :param file_extension: The file extension that the submitted file should have.
    :return: Success or error message - Type: String
    """
    s3 = boto3.resource('s3', region_name='eu-west-2')
    try:
        full_file_name = file_name + file_extension
        if len(file_prefix) > 0:
            full_file_name = file_prefix + full_file_name

        s3.Object(bucket_name, full_file_name).load()
        s3.Object(bucket_name, full_file_name).delete()
        return "Succesfully deleted file from S3 bucket."
    except ClientError:
        return "File does not exist in specified bucket!"


def get_data(queue_url, bucket_name, key, incoming_message_group, file_prefix="",
             file_extension=".json"):
    """
    Get data function recieves a message from an sqs queue,
    extracts the bucket and filename, then uses them to get the file from s3.
    If no messages are in the queue, or if the message does not come
    from the preceding module, the bucket_name and key given as parameters are used
    instead.

    SQS only supports message length of 256k, so this function is to be used instead of
    get_sqs_message when the data size approaches this figure. Used in conjunction with
    save_data

    Data is returned as a json string. To use as dataframe you will need to json.loads
    and pd.dataframe() the response.
    :param queue_url: The url of the queue to retrieve message from - Type: String
    :param bucket_name: The default bucket name to use if no message from previous
    module - Type: String
    :param key: The default file name to use if no message from the previous
    module - Type: String
    :param incoming_message_group: The name of the message group from previous
    module - Type: String
    :param file_prefix: Optional, run id to be added as file name prefix - Type: String
    :param file_extension: The file extension that the submitted file should have.
    :return data: The data from s3 - Type: Json
    :return receipt_handle: The receipt_handle of the incoming message
    (used to delete old message) - Type: String
    """
    response = get_sqs_message(queue_url)
    receipt_handle = None
    if "Messages" not in response or (
        "Messages" in response
        and (
            response["Messages"][0]["Attributes"]["MessageGroupId"]
            != incoming_message_group
        )
    ):
        bucket = bucket_name
        key = key
        data = read_from_s3(bucket, key)
    else:
        message = response["Messages"][0]
        receipt_handle = message["ReceiptHandle"]
        message = json.loads(message["Body"])
        bucket = message["bucket"]
        key = message["key"]
        data = read_from_s3(bucket, key, file_prefix, file_extension)
    return data, receipt_handle


def get_dataframe(queue_url, bucket_name, key, incoming_message_group, file_prefix="",
                  file_extension=".json"):
    """
    Get data function recieves a message from an sqs queue,
    extracts the bucket and filename, then uses them to get the file from s3.
    If no messages are in the queue, or if the message does not come
    from the preceding module, the bucket_name and key given as parameters are used
    instead.

    SQS only supports message length of 256k, so this function is to be used instead of
    get_sqs_message when the data size approaches this figure. Used in conjunction with
    save_data

    Data is returned as a DataFrame.

    :param queue_url: The url of the queue to retrieve message from - Type: String
    :param bucket_name: The default bucket name to use if no message from previous
    module - Type: String
    :param key: The default file name to use if no message from the previous
    module - Type: String
    :param incoming_message_group: The name of the message group from previous
    module - Type: String
    :param file_prefix: Optional, run id to be added as file name prefix - Type: String
    :param file_extension: The file extension that the submitted file should have.
    :return data: The data from s3 - Type: DataFrame
    :return receipt_handle: The receipt_handle of the incoming message
    (used to delete old message) - Type: String
    """
    data, receipt_handle = get_data(queue_url, bucket_name, key,
                                    incoming_message_group, file_prefix, file_extension)
    data = pd.read_json(data, dtype=False)
    return data, receipt_handle


def get_sqs_message(queue_url, max_number_of_messages=1):
    """
    This method retrieves the data from the specified SQS queue.
    :param queue_url: The url of the SQS queue. - Type: String
    :param max_number_of_messages: Number of messages to pick up from queue(default 1)
     - Type: Int
    :return: Messages from queue - Type: json string
    """
    sqs = boto3.client("sqs", region_name="eu-west-2")
    return sqs.receive_message(QueueUrl=queue_url, AttributeNames=["MessageGroupId"],
                               MaxNumberOfMessages=max_number_of_messages)


def get_sqs_messages(sqs_queue_url, number_of_messages, incoming_message_group):
    """
    This method retrieves a number of messages from the sqs queue.
    It takes 10 messages from the queue, then checks each to see if it comes from
    the appropriate message_group.

    :param sqs_queue_url: The url of the SQS queue. - Type: String
    :param number_of_messages: Number of messages expected
                (will raise error if not met): Type - Int
    :param incoming_message_group: The message group of messages to collect.
    :return: Messages from queue - List of Json Strings
    """
    messages = {"Messages": []}
    # Grab 10 messages from queue
    responses = get_sqs_message(sqs_queue_url, 10)
    if "Messages" not in responses:
        raise exception_classes.NoDataInQueueError("No Messages in queue")
    # Loop through the messages to see if they fit criteria
    for response in responses['Messages']:
        if incoming_message_group in response['Attributes']['MessageGroupId']:
            messages["Messages"].append(response)
    if len(messages['Messages']) < number_of_messages:
        raise exception_classes.DoNotHaveAllDataError(
            "Only " + str(len(messages["Messages"])) + " recieved"
        )
    return messages


def read_dataframe_from_s3(bucket_name, file_name, file_prefix="",
                           file_extension=".json"):
    """
    Given the name of the bucket and the filename(key), this function will
    return contents of a file. File is DataFrame format.
    :param bucket_name: Name of the S3 bucket - Type: String
    :param file_name: Name of the file - Type: String
    :param file_prefix: Optional, run id to be added as file name prefix - Type: String
    :param file_extension: The file extension that the submitted file should have.
    :return: input_file: The JSON file in S3 loaded into dataframe table - Type: DataFrame
    """
    input_file = read_from_s3(bucket_name, file_name, file_prefix, file_extension)
    json_content = json.loads(input_file)
    return pd.DataFrame(json_content)


def read_from_s3(bucket_name, file_name, file_prefix="", file_extension=".json"):
    """
    Given the name of the bucket and the filename(key), this function will
    return a file. File is JSON format.
    :param bucket_name: Name of the S3 bucket - Type: String
    :param file_name: Name of the file - Type: String
    :param file_prefix: Optional, run id to be added as file name prefix - Type: String
    :param file_extension: The file extension that the submitted file should have.
    :return: input_file: The JSON file in S3 - Type: String
    """
    s3 = boto3.resource("s3", region_name="eu-west-2")
    full_file_name = file_name + file_extension
    if len(file_prefix) > 0:
        full_file_name = file_prefix + full_file_name
    try:
        s3_object = s3.Object(bucket_name, full_file_name)
        input_file = s3_object.get()["Body"].read().decode("UTF-8")
    except Exception as e:
        raise Exception(f"Could not find s3://{bucket_name}/{full_file_name}.{type(e)}")
    return input_file


def save_data(bucket_name, file_name, data, queue_url, message_id, file_prefix="",
              file_extension=".json"):
    """
    Save data function stores data in s3 and passes the bucket & filename
    onto sqs queue. SQS only supports message length of 256k, so this function
     is to be used instead of send_sqs_message
     when the data size approaches this figure. Used in conjunction with get_data
    :param bucket_name: The name of the s3 bucket to use to save data
    - Type: String
    :param file_name: The name to give the file being saved - Type: String
    :param data: The data to be saved - Type Json string
    :param queue_url: The url of the queue to use in sending the file details
    - Type: String
    :param message_id: The label of the message sent to sqs(Message_group_id,
    what module sent the message)
    - Type: String
    :param file_prefix: Optional, run id to be added as file name prefix - Type: String
    :param file_extension: The file extension that the submitted file should have.
    :return: Nothing
    """
    save_to_s3(bucket_name, file_name, data, file_prefix, file_extension)
    sqs_message = json.dumps({"bucket": bucket_name, "key": file_name})
    send_sqs_message(queue_url, sqs_message, message_id)


def save_dataframe_to_csv(dataframe, bucket_name, file_name, file_prefix="",
                          file_extension=".csv"):
    """
    This function takes a Dataframe and stores it in a specific bucket.
    :param dataframe: The Dataframe you wish to save - Type: Dataframe.
    :param bucket_name: Name of the bucket you wish to save the csv into - Type: String.
    :param file_name: The name given to the CSV - Type: String.
    :param file_prefix: Optional, run id to be added as file name prefix - Type: String
    :param file_extension: The file extension that the submitted file should have.
    :return: None
    """
    csv_buffer = StringIO()
    dataframe.to_csv(csv_buffer, sep=",", index=False)
    data = csv_buffer.getvalue()

    save_to_s3(bucket_name, file_name, data, file_prefix, file_extension)


def save_to_s3(bucket_name, output_file_name, output_data, file_prefix="",
               file_extension=".json"):
    """
    This function uploads a specified set of data to the s3 bucket under the given name.
    :param bucket_name: Name of the bucket you wish to upload too - Type: String.
    :param output_file_name: Name you want the file to be called on s3 - Type: String.
    :param output_data: The data that you wish to upload to s3 - Type: JSON.
    :param file_prefix: Optional, run id to be added as file name prefix - Type: String
    :param file_extension: The file extension that the submitted file should have.
    :return: None
    """
    s3 = boto3.resource("s3", region_name="eu-west-2")

    full_file_name = output_file_name + file_extension
    if len(file_prefix) > 0:
        full_file_name = file_prefix + full_file_name

    s3.Object(bucket_name, full_file_name).put(
        Body=output_data, ContentType=extension_types[file_extension])


def send_bpm_status(queue_url, module_name, status, run_id, current_step_num="-",
                    total_steps="6"):
    """
    This function is to provide status updates to the user via the BPM layer. Currently
    it is set up to place the message on an SQS queue for BPM to pick up.
    :param queue_url: Name of the queue for the BMP layer - Type: String.
    :param module_name: Current module name - Type: String.
    :param status: Current status of the module IN PROGRESS, FINISHED, FAILED
    - Type: String.
    :param run_id: run id of current run passed from the module - Type: String
    :param current_step_num: Number of the current module step in sequence - Type String.
    :param total_steps: Total number of steps in the system
    :return: None
    """
    output_message = "_BMI_Status_Message"
    output_message_id = run_id + output_message

    bpm_message = {
        "bpm_id": run_id,
        "status": {
            "current_step": current_step_num,
            "total_steps": total_steps,
            "step_name": module_name,
            "message": {
                "text": module_name + " stage: " + status
            },
            "state": status}
    }

    bpm_message = json.dumps(bpm_message)

    send_sqs_message(queue_url, bpm_message, output_message_id)


def send_sns_message(sns_topic_arn, module_name):
    """
    This method is responsible for sending a notification to the specified arn,
    so that it can be used to relay information for the BPM to use and handle.
    :param module_name: The name of the module currently being run - Type: String.
    :param sns_topic_arn: The arn of the sns topic you are directing the message at -
                          Type: String.
    :return: Json string containing metadata about the message.
    """
    sns = boto3.client("sns", region_name="eu-west-2")
    sns_message = {
        "success": True,
        "module": module_name,
        "message": "Completed " + module_name,
    }

    return sns.publish(TargetArn=sns_topic_arn, Message=json.dumps(sns_message))


def send_sns_message_with_anomalies(anomalies, sns_topic_arn, module_name):
    """
    This method is responsible for sending a notification to the specified arn,
    so that it can be used to relay information for the BPM to use and handle.
    :param anomalies: Json formatted summary of data anomalies - Type: String.
    :param module_name: The name of the module currently being run - Type: String.
    :param sns_topic_arn: The arn of the sns topic you are directing the message at -
                          Type: String.
    :return: None
    """
    sns = boto3.client("sns", region_name="eu-west-2")
    sns_message = {
        "success": True,
        "module": module_name,
        "anomalies": anomalies,
        "message": "Completed " + module_name,
    }

    sns.publish(TargetArn=sns_topic_arn, Message=json.dumps(sns_message))


def send_sqs_message(queue_url, message, output_message_id):
    """
    This method is responsible for sending data to the SQS queue.
    :param queue_url: The url of the SQS queue. - Type: String
    :param message: The message/data you wish to send to the SQS queue - Type: String
    :param output_message_id: The label of the record in the SQS queue - Type: String
    :return: Json string containing metadata about the message.
    """
    # MessageDeduplicationId is set to a random hash to overcome de-duplication,
    # otherwise modules could not be re-run in the space of 5 Minutes.
    sqs = boto3.client("sqs", region_name="eu-west-2")
    return sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=message,
        MessageGroupId=output_message_id,
        MessageDeduplicationId=str(random.getrandbits(128)),
    )
