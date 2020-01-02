def calculate_adjacent_periods(current_period, periodicity):
    """
    Description: This method uses periodicity to calculate
    what should be the adjacent periods for a row,
    Then uses a filter to confirm whether these periods exist for a record.
    :param current_period: int/str(either) - The current period to find the previous for
    :param periodicity: String - The periodicity of the survey we are imputing for:
    01 = monthly, 02 = annually, 03 = quarterly
    :return: previous_period: String - The previous period.
    """
    monthly = "01"
    annually = "02"
    current_month = str(current_period)[4:]
    current_year = str(current_period)[:4]
    if periodicity == monthly:

        last_month = int(float(current_month)) - int(periodicity)
        last_year = int(current_year)
        if last_month < 1:
            last_year -= 1
            last_month += 12
        if last_month < 10:
            last_month = "0" + str(last_month)

        last_period = str(last_year) + str(last_month)

    elif periodicity == annually:

        last_period = str(int(current_period) - 1)

    else:  # quarterly(03)

        last_month = int(current_month) - 3
        last_year = int(current_year)
        if last_month < 1:
            last_year -= 1
            last_month += 4
        if len(str(last_month)) < 2:
            last_month = "0" + str(last_month)
        last_period = str(last_year) + str(last_month)

    return last_period
