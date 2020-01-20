# Test Module Example <a name='top'>
[Back](README.md)

## Description
Here is a copy of the generic tests being used in the Enrichment module.
Most modules should be able to use a copy of this with different parameters.

Note that for the generic tests to be used the runtime and evironment variables need to be read in before anytime else is done. Also when passing parameters into the method you need to ensure they are wrapped in a "RuntimeVariables": {'Parameters Go Here'}

## Example Class
```
class GenericErrors(unittest.TestCase):

    @parameterized.expand([
        (lambda_method_function, method_runtime_variables,
         method_environment_variables, "tests/fixtures/test_method_input.json"),
        (lambda_wrangler_function, wrangler_runtime_variables,
         wrangler_environment_variables, None)
    ])
    def test_client_error(self, which_lambda, which_runtime_variables,
                          which_environment_variables, which_data):
        test_generic_library.client_error(which_lambda, which_runtime_variables,
                                          which_environment_variables, which_data)

    @parameterized.expand([
        (lambda_method_function, method_runtime_variables,
         method_environment_variables, "enrichment_method.EnvironSchema"),
        (lambda_wrangler_function, wrangler_runtime_variables,
         wrangler_environment_variables, "enrichment_wrangler.EnvironSchema")
    ])
    def test_general_error(self, which_lambda, which_runtime_variables,
                           which_environment_variables, chosen_exception):
        test_generic_library.general_error(which_lambda, which_runtime_variables,
                                           which_environment_variables, chosen_exception)

    @mock_s3
    @mock.patch('enrichment_wrangler.aws_functions.get_dataframe',
                side_effect=test_generic_library.replacement_get_dataframe)
    def test_incomplete_read_error(self, mock_s3_get):

        file_list = ["test_wrangler_input.json"]

        test_generic_library.incomplete_read_error(lambda_wrangler_function,
                                                   wrangler_runtime_variables,
                                                   wrangler_environment_variables,
                                                   file_list,
                                                   "enrichment_wrangler")

    @parameterized.expand([
        (lambda_method_function, method_environment_variables),
        (lambda_wrangler_function, wrangler_environment_variables)
    ])
    def test_key_error(self, which_lambda, which_environment_variables):
        test_generic_library.key_error(which_lambda, which_environment_variables, bad_runtime_variables)

    @mock_s3
    @mock.patch('enrichment_wrangler.aws_functions.get_dataframe',
                side_effect=test_generic_library.replacement_get_dataframe)
    def test_method_error(self, mock_s3_get):

        file_list = ["test_wrangler_input.json"]

        test_generic_library.method_error(lambda_wrangler_function,
                                          wrangler_runtime_variables,
                                          wrangler_environment_variables,
                                          file_list,
                                          "enrichment_wrangler")

    @parameterized.expand([(lambda_method_function, ), (lambda_wrangler_function, )])
    def test_value_error(self, which_lambda):
        test_generic_library.value_error(
            which_lambda, bad_runtime_variables, bad_environment_variables
        )

```
[Back to top](#top)
<hr>
