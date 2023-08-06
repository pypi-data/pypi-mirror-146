from datetime import datetime

import dateparser as dateparser
from dateutil.parser import parser

from source.visualiser.column_data.base_column_data_type import BaseColumnDataType
from source.visualiser.exceptions import InputValueException


class ColumnDataItemIntegerFromString(BaseColumnDataType):
    def interpret_column_value(self, input_value):
        return int(input_value)


class ColumnDataItemIntegerFromInteger(BaseColumnDataType):
    def interpret_column_value(self, input_value):
        return input_value


class ColumnDataItemBooleanFromBoolean(BaseColumnDataType):
    def interpret_column_value(self, input_value):
        return input_value


class ColumnDataItemTextFromText(BaseColumnDataType):
    def interpret_column_value(self, input_value):
        return input_value


class ColumnDataItemDateFromDate(BaseColumnDataType):
    def interpret_column_value(self, input_value):
        # need to ensure that date is only the date, not time.
        return input_value.date()


class ColumnDataItemDateFromMSPString(BaseColumnDataType):
    """
    Specifically converts from strings exports by MSP
    """
    def interpret_column_value(self, input_value):
        # Strip off extraneous time information at the end of the string
        stripped_date_string = input_value[:-6]
        return datetime.strptime(stripped_date_string, '%d %B %Y').date()


class ColumnDataItemBooleanFromYesNo(BaseColumnDataType):
    """
    Converts from srting "Yes/No" to boolean (not case sensitive)
    """
    def interpret_column_value(self, input_value):
        input_lower = input_value.lower()
        if input_lower == "yes":
            return True
        elif input_lower == "no":
            return False
        else:
            raise InputValueException(f"Expecting 'yes' or 'no' but got {input_value}")


class ColumnDataItemIntegerFromText(BaseColumnDataType):
    """
    MSP exports duration as a string field of the form "nnn Days" (possibly other unit as well but I have only seen
    days).

    So extract the numerical value and convert to int.  The app expects duration to be in days.
    """
    def interpret_column_value(self, input_value):
        if input_value is None:
            int_value = None
        else:
            int_value = int(input_value)

        return int_value


class ColumnDataItemIntegerFromMspDurationText(BaseColumnDataType):
    """
    MSP exports duration as a string field of the form "nnn Days" (possibly other unit as well but I have only seen
    days).

    So extract the numerical value and convert to int.  The app expects duration to be in days.
    """
    def interpret_column_value(self, input_value):
        int_string_position = input_value.find(' ')
        int_string = int(input_value[:int_string_position])
        int_value = int(int_string)

        return int_value


