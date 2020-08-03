# General Functions <a name='top'>
[Back](README.md)
## Contents
[Calculate Adjacent Periods](#calculateadjacentperiods)<br>
[Handle Exception](#handleexception)<br>
[SAS Round](#sasround)<br>
[Get logger](#getlogger)<br>
## Functions
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

### Handle Exception <a name='handleexception'>
Generates an error message from an exception.
Returns an error message detailing exception type, arguments, and line number.
#### Parameters:
exception: Exception that has occurred - Type: Exception<br>
module: Name of current module - Type: String<br>
context: AWS Context object<br>
    (has default so that moving to glue will not require lots of changes)
#### Return:
error_message: Error message generated for exception - Type: String

#### Usage:
```
try:
    myfunc()
except Exception as e:
    print(general_functions.handle_exception(e, 'mikemodule', context))
    
    ------------------
    
    logger.info(general_functions.handle_exception(e, 'mikemodule'))```
```
[Back to top](#top)
<hr>

### SAS Round <a name='sasround'>
Replicates the sas rounding method by not rounding to nearest even.

#### Parameters:
num: Decimal number to round - Type: Float

#### Return:
num: Rounded number - Type: Int

#### Usage:
```
general_functions.sas_round(x["prev_" + question] * x["imputation_factor_" + question]),
```

[Back to top](#top)
<hr>

### Get Logger <a name='getlogger'>
Returns a logger with loglevel set. Will attempt to get log level from environment, defaults to info.

#### Parameters:

---

#### Return:
logger: The logger - Type: Logger

#### Usage:
```
logger = general_functions.get_logger(),
```

[Back to top](#top)
<hr>
