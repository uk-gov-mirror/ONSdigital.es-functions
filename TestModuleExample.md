# Test Module Example <a name='top'>
[Back](README.md)

## Description
Here is a copy of the generic tests being used in the Enrichment module.
Most modules should be able to use a copy of this with different parameters.

Note that for the generic tests to be used the runtime and evironment variables need to be read in before anytime else is done. Also when passing parameters into the method you need to ensure they are wrapped in a "RuntimeVariables": {'Parameters Go Here'}

## Example Class
```
##########################################################################################
#                                     Generic                                            #
##########################################################################################


def test_wrangler_client_error():
    test_generic_library.wrangler_client_error(lambda_wrangler_function,
                                               wrangler_runtime_variables,
                                               wrangler_environment_variables,
                                               None)


def test_method_client_error():
    test_generic_library.method_client_error(lambda_method_function,
                                             method_runtime_variables,
                                             method_environment_variables,
                                             "tests/fixtures/test_method_input.json")


def test_wrangler_general_error():
    test_generic_library.wrangler_general_error(lambda_wrangler_function,
                                                wrangler_runtime_variables,
                                                wrangler_environment_variables,
                                                "enrichment_wrangler.EnvironSchema")


def test_method_general_error():
    test_generic_library.method_general_error(lambda_method_function,
                                              method_runtime_variables,
                                              method_environment_variables,
                                              "enrichment_method.EnvironSchema")


@mock_s3
@mock.patch('enrichment_wrangler.aws_functions.get_dataframe',
            side_effect=test_generic_library.replacement_get_dataframe)
def test_incomplete_read_error(mock_s3_get):
    file_list = ["test_wrangler_input.json"]

    test_generic_library.incomplete_read_error(lambda_wrangler_function,
                                               wrangler_runtime_variables,
                                               wrangler_environment_variables,
                                               file_list,
                                               "enrichment_wrangler")


def test_wrangler_key_error():
    test_generic_library.wrangler_key_error(lambda_wrangler_function, wrangler_environment_variables)


def test_method_key_error():
    test_generic_library.method_key_error(lambda_method_function, method_environment_variables)


@mock_s3
@mock.patch('enrichment_wrangler.aws_functions.get_dataframe',
            side_effect=test_generic_library.replacement_get_dataframe)
def test_method_error(mock_s3_get):
    file_list = ["test_wrangler_input.json"]

    test_generic_library.wrangler_method_error(lambda_wrangler_function,
                                      wrangler_runtime_variables,
                                      wrangler_environment_variables,
                                      file_list,
                                      "enrichment_wrangler")


def test_wrangler_value_error():
    test_generic_library.wrangler_value_error(lambda_wrangler_function)


def test_method_value_error():
    test_generic_library.method_value_error(lambda_method_function)

```
[Back to top](#top)
<hr>
