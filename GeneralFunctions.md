# General Functions <a name='top'>
[Back](README.md)
## Contents
[Calculate Adjacent Periods](#calculateadjacentperiods)<br>
[Sas Round](#sasround)<br>
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

### Sas Round <a name='sasround'>
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
