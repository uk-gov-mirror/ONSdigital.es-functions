import io
import json
from unittest import mock

import boto3
import pytest
from es_aws_functions import aws_functions, exception_classes


class MockContext:
    aws_request_id = 999


bad_environment_variables = {}

bad_runtime_variables = {}

incomplete_runtime_variables = {
    "RuntimeVariables": {"run_id": "run_id"}
}

context_object = MockContext()


def method_assert(lambda_function, runtime_variables, expected_message):
    """
    Function to perform sad path assertion on methods
    (method sad path is different to wrangler)

    Runs function to get output, then checks output.
    :param lambda_function: Lambda function to test - Type: Function
    :param runtime_variables: Runtime variables to send to function - Type: Dict
    :param expected_message: The error message that is expected from the test
    - Type: String
    :return Test Pass/Fail
    """
    output = lambda_function.lambda_handler(runtime_variables, context_object)
    assert 'error' in output.keys()
    assert expected_message in output["error"]


def wrangler_assert(lambda_function, runtime_variables, expected_message):
    """
    Function to perform sad path assertion on wrangler
    (method sad path is different to wrangler)

    Runs function and asserts that exception is raised, then checks the contents.
    :param lambda_function: Lambda function to test - Type: Function
    :param runtime_variables: Runtime variables to send to function - Type: Dict
    :param expected_message: The error message that is expected from the test
    - Type: String
    :return Test Pass/Fail
    """
    with pytest.raises(exception_classes.LambdaFailure) as exc_info:
        lambda_function.lambda_handler(runtime_variables, context_object)
    assert expected_message in exc_info.value.error_message


def client_error(lambda_function, runtime_variables,
                 environment_variables, file_name,
                 expected_message, assertion):
    """
    Function to trigger a client error in a function.
    By not mocking any of the boto3 functions, once any are used in code they will
    trigger client error due to lack of credentials.

    If used on a method, data is part of the runtime_variables, so the file_name is loaded
    in and the file added to the runtime_variables dictionary.
    :param lambda_function: Lambda function to test - Type: Function
    :param runtime_variables: Runtime variables to send to function - Type: Dict
    :param environment_variables: Environment Vars to send to function - Type: Dict
    :param file_name: Name of file to retrieve data from - Type: String
    :param expected_message: The error message that is expected from the test
    - Type: String
    :param assertion: Type of assertion to use - Type: Function
    :return Test Pass/Fail
    """
    if "data" in runtime_variables["RuntimeVariables"].keys():
        with open(file_name, "r") as file:
            test_data = file.read()
        runtime_variables["RuntimeVariables"]["data"] = test_data

    if not environment_variables:
        assertion(lambda_function, runtime_variables, expected_message)
    else:
        with mock.patch.dict(lambda_function.os.environ, environment_variables):
            assertion(lambda_function, runtime_variables, expected_message)


def create_bucket(bucket_name):
    """
    Create an s3 bucket.
    :param bucket_name: Name of bucket to create - Type: String
    :return client: S3 client that created bucket - Type: Boto3 Client
    """
    client = create_client("s3")
    client.create_bucket(Bucket=bucket_name)
    return client


def create_client(client_type, region="eu-west-2"):
    """
    Create a boto3 client for use with aws tests.
    :param client_type: Type of client(eg. s3, lambda, sqs etc) - Type: String
    :param region: Region to create client in(default is eu-west-2) - Type: String
    :return client: Requested boto3 client - Type: Boto3 Client
    """
    client = boto3.client(
      client_type,
      region_name=region,
      aws_access_key_id="fake_access_key",
      aws_secret_access_key="fake_secret_key",
      )
    return client


def general_error(lambda_function, runtime_variables,
                  environment_variables, mockable_function,
                  expected_message, assertion):
    """
    Function to trigger a general error in a given wrangler.

    The variable 'mockable_function' defines the function in the lambda that will
    be mocked out. This should be something fairly early in the code (but still
    within try/except). e.g. "enrichment_wrangler.EnvironSchema"
    :param lambda_function: Lambda function to test - Type: Function
    :param runtime_variables: Runtime variables to send to function - Type: Dict
    :param environment_variables: Environment Vars to send to function - Type: Dict
    :param mockable_function: The function in the code to mock out
            (and attach side effect to) - Type: String
    :param expected_message: The error message that is expected from the test
    - Type: String
    :param assertion: Type of assertion to use - Type: Function
    :return Test Pass/Fail
    """
    with mock.patch(mockable_function) as mock_schema:
        mock_schema.side_effect = Exception("Failed To Log")

        if not environment_variables:
            assertion(lambda_function, runtime_variables, expected_message)
        else:
            with mock.patch.dict(lambda_function.os.environ, environment_variables):
                assertion(lambda_function, runtime_variables, expected_message)


def incomplete_read_error(lambda_function, runtime_variables,
                          environment_variables, file_list, wrangler_name,
                          expected_message="Incomplete Lambda response"):
    """
    Function to trigger an incomplete read error in a given wrangler.

    Takes in a valid file(s) so that the function performs until after the lambda invoke.

    The data that triggers the incomplete_read is generic, so hardcoded as a variable.

    :param lambda_function: Lambda function to test - Type: Function
    :param runtime_variables: Runtime variables to send to function - Type: Dict
    :param environment_variables: Environment Vars to send to function - Type: Dict
    :param file_list: List of input files for the function - Type: List
    :param wrangler_name: Wrangler that is being tested,
            used in mocking boto3. - Type: String
    :param expected_message: - Error message we are expecting. - Type: String
            (default to match current exception handling)
    :return Test Pass/Fail
    """

    bucket_name = environment_variables["bucket_name"]
    client = create_bucket(bucket_name)
    upload_files(client, bucket_name, file_list)

    with mock.patch(wrangler_name + ".boto3.client") as mock_client:
        mock_client_object = mock.Mock()
        mock_client.return_value = mock_client_object

        test_data_bad = io.BytesIO(b'{"Bad Bytes": 999}')
        mock_client_object.invoke.return_value = {
            "Payload": StreamingBody(test_data_bad, 1)}
        with pytest.raises(exception_classes.LambdaFailure) as exc_info:
            if not environment_variables:
                lambda_function.lambda_handler(runtime_variables, context_object)
            else:
                with mock.patch.dict(lambda_function.os.environ, environment_variables):
                    lambda_function.lambda_handler(runtime_variables, context_object)

        assert expected_message in exc_info.value.error_message


def key_error(lambda_function,
              environment_variables,
              expected_message, assertion,
              runtime_variables=bad_runtime_variables,
              ):
    """
    Function to trigger a key error in a given method.
    Makes use of an empty dict of runtime variables,
    which triggers a key error once access is attempted.
    :param lambda_function: Lambda function to test - Type: Function
    :param environment_variables: Environment Vars to send to function - Type: Dict
    :param expected_message: The error message that is expected from the test
    - Type: String
    :param assertion: Type of assertion to use - Type: Function
    :param runtime_variables: Runtime variables to send to function
                            (default is empty dict) - Type: Dict
    :return Test Pass/Fail
    """
    if not environment_variables:
        assertion(lambda_function, runtime_variables, expected_message)
    else:
        with mock.patch.dict(lambda_function.os.environ, environment_variables):
            assertion(lambda_function, runtime_variables, expected_message)


def replacement_get_dataframe(sqs_queue_url, bucket_name,
                              in_file_name, incoming_message_group,
                              file_prefix="", file_extension=""):
    """
    Function to replace the aws-functions.get_dataframe when performing tests.

    Instead of getting an sqs message and then using it to define the file to get,
    Goes straight to s3 for the data. Variables marked as 'Unused' are variables that the
    original function needed by the replacement one doesn't.

    Takes the same parameters as get_dataframe, but only uses file_name and data.
    :param sqs_queue_url: Name of sqs queue. Unused
    :param bucket_name: Name of bucket to retrieve data from - Type: String
    :param in_file_name: Name of file to read in - Type: String
    :param incoming_message_group: Name of message group. Unused
    :param file_prefix: Optional, run id to be added as file name prefix. Unused
    :param file_extension: The file extension that the submitted file should have. Unused
    :return data: Data from file - Type: Dataframe
    :return receipt: Int to simulate message receipt - Type: Int
    """
    data = aws_functions.read_dataframe_from_s3(bucket_name, in_file_name)

    return data, 999


def replacement_invoke(FunctionName, Payload):  # noqa N803
    """
    Function to replace the lambda invoke, it instead saves data to be compared.
    Takes the same parameters as get_dataframe, but only uses file_name and data.
    :param FunctionName: Name of the lambda to be invoked. Unused
    :param Payload: The passed in parameters and data for the original invoke.
    :return None
    """
    runtime = json.loads(Payload)["RuntimeVariables"]
    data = runtime["data"]
    if type(data) == list:
        data = json.dumps(data)

    with open('tests/fixtures/test_wrangler_to_method_input.json', 'w',
              encoding='utf-8') as f:
        f.write(json.dumps(json.loads(data), indent=4, sort_keys=True))
        f.close()

    runtime["data"] = None

    with open('tests/fixtures/test_wrangler_to_method_runtime.json', 'w',
              encoding='utf-8') as f:
        f.write(json.dumps(runtime, indent=4, sort_keys=True))
        f.close()


def replacement_save_data(bucket_name, file_name, data,
                          sqs_queue_url, sqs_message_id,
                          file_prefix="", file_extension=""):
    """
    Function to replace the aws-functions.save_data when performing tests.

    Saves a copy of the file locally.

    Takes the same parameters as save_data, but only uses file_name and data.
    :param bucket_name: Name of bucket. Unused.
    :param file_name: Name of file to save in tests/fixtures - Type: String
    :param data: Data to save - Type: Json String
    :param sqs_queue_url: Name of sqs queue. Unused
    :param sqs_message_id: Name of message group. Unused
    :param file_prefix: Optional, run id to be added as file name prefix. Unused
    :param file_extension: The file extension that the submitted file should have. Unused
    :return None
    """
    with open("tests/fixtures/" + file_name, 'w', encoding='utf-8') as f:
        f.write(json.dumps(json.loads(data), indent=4, sort_keys=True))
        f.close()


def replacement_save_to_s3(bucket_name, file_name, data,
                           file_prefix="", file_extension=""):
    """
    Function to replace the aws-functions.save_data when performing tests.

    Saves a copy of the file locally.

    Takes the same parameters as save_data, but only uses file_name and data.
    :param bucket_name: Name of bucket. Unused.
    :param file_name: Name of file to save in tests/fixtures - Type: String
    :param data: Data to save - Type: Json String
    :param file_prefix: Optional, run id to be added as file name prefix. Unused
    :param file_extension: The file extension that the submitted file should have. Unused
    :return None
    """
    with open("tests/fixtures/" + file_name, 'w', encoding='utf-8') as f:
        f.write(json.dumps(json.loads(data), indent=4, sort_keys=True))
        f.close()


def upload_files(client, bucket_name, file_list):
    """
    Upload a list of files to a given s3 bucket from the test/fixtures folder.
    Key of the uploaded file(s) is their filename.
    :param client: S3 Client - Type: Boto3 Client
    :param bucket_name: Name of bucket to place files in - Type: String
    :param file_list: List of files to upload - Type: List
    :return client: S3 client that uploaded files
    """
    for file in file_list:
        client.upload_file(
            Filename="tests/fixtures/" + file,
            Bucket=bucket_name,
            Key=file,
        )
    return client


def value_error(lambda_function, expected_message, assertion,
                runtime_variables=incomplete_runtime_variables,
                environment_variables=bad_environment_variables):
    """
    Function to trigger a value error in a given method.
    Does so by passing an empty list of environment variables
    to trigger an error with marshmallow.
    :param lambda_function: Lambda function to test - Type: Function
    :param expected_message: The error message that is expected from the test
    - Type: String
    :param assertion: Type of assertion to use - Type: Function
    :param runtime_variables: Runtime variables to send to function - Type: Dict
    :param environment_variables: Environment Vars to send to function - Type: Dict
    :return Test Pass/Fail
    """
    if not environment_variables:
        assertion(lambda_function, runtime_variables, expected_message)
    else:
        with mock.patch.dict(lambda_function.os.environ, environment_variables):
            assertion(lambda_function, runtime_variables, expected_message)


def wrangler_method_error(lambda_function, runtime_variables,
                          environment_variables, file_list, wrangler_name):
    """
    Function to trigger a method error in a given function.

    Takes in a valid file(s) so that the function performs until after the lambda invoke.

    :param lambda_function: Lambda function to test - Type: Function
    :param runtime_variables: Runtime variables to send to function - Type: Dict
    :param environment_variables: Environment Vars to send to function - Type: Dict
    :param file_list: List of input files for the function - Type: List
    :param wrangler_name: Wrangler that is being tested,
            used in mocking boto3. - Type: String
    :return Test Pass/Fail
    """

    bucket_name = environment_variables["bucket_name"]
    client = create_bucket(bucket_name)
    upload_files(client, bucket_name, file_list)

    with mock.patch(wrangler_name + ".boto3.client") as mock_client:
        mock_client_object = mock.Mock()
        mock_client.return_value = mock_client_object

        mock_client_object.invoke.return_value.get.return_value \
            .read.return_value.decode.return_value = \
            json.dumps({"error": "Test Message",
                        "success": False})
        with pytest.raises(exception_classes.LambdaFailure) as exc_info:
            if not environment_variables:
                lambda_function.lambda_handler(runtime_variables, context_object)
            else:
                with mock.patch.dict(lambda_function.os.environ, environment_variables):
                    lambda_function.lambda_handler(runtime_variables, context_object)
        assert "Test Message" in exc_info.value.error_message
