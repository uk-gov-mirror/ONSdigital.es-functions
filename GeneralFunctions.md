# General Functions <a name='top'>
## Contents
[Calculate Adjacent Periods](#calculateadjacentperiods)<br>
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
