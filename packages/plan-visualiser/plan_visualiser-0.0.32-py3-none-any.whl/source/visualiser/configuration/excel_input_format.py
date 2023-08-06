from source.visualiser.column_data.column_data_item_integer_from_string import ColumnDataItemBooleanFromBoolean, \
    ColumnDataItemTextFromText, ColumnDataItemIntegerFromInteger, ColumnDataItemDateFromDate, \
    ColumnDataItemBooleanFromYesNo, ColumnDataItemIntegerFromMspDurationText, ColumnDataItemDateFromMSPString, \
    ColumnDataItemIntegerFromText
from source.visualiser.exceptions import ColumnNameException


class ExcelInputFormat:
    def __init__(self, column_mapping):
        self.column_mapping = column_mapping

    def decode_column(self, input_column_name, input_value):
        decode_class = self.column_mapping[input_column_name][1]
        decode_object = decode_class(input_value)
        return decode_object.value

    def input_column_names(self):
        """
        Generates a list of column names to import, used in the reading of the Excel file.

        :return:
        """
        return [record[0] for key, record in self.column_mapping.items()]

    def input_column_name(self, column_name):
        column_names = [input_col_record[0] for col_name, input_col_record in self.column_mapping.items() if col_name == column_name]
        if len(column_names) != 1:
            raise ColumnNameException(f"Number of matches to column name should be exactly one, was {len(column_names)}")
        input_column_name = column_names[0]
        return input_column_name

    def extract_column_value(self, data_row, column_name):
        input_column_name = self.input_column_name(column_name)
        input_value = data_row[input_column_name]
        decoded_value = self.decode_column(
            column_name,
            input_value
        )
        return decoded_value


excel_smartsheet_driver = ExcelInputFormat({
        'task_name': ('Task Name', ColumnDataItemTextFromText),
        'visual_flag': ('Visual Flag', ColumnDataItemBooleanFromBoolean),
        'visual_text': ('Visual Text', ColumnDataItemTextFromText),
        'swimlane': ('Visual Swimlane', ColumnDataItemTextFromText),
        'duration': ('Duration', ColumnDataItemIntegerFromInteger),
        'start_date': ('Start', ColumnDataItemDateFromDate),
        'end_date': ('Finish', ColumnDataItemDateFromDate),
        'num_track_within_swimlane': ('Visual Track # Within Swimlane', ColumnDataItemIntegerFromInteger),
        'num_tracks_to_cover': ('Visual # Tracks To Cover', ColumnDataItemIntegerFromInteger),
        'text_layout': ('Text Layout', ColumnDataItemTextFromText),
        'outstanding_format_name': ('Format String', ColumnDataItemTextFromText),
        'complete_format_name': ('Done Format String', ColumnDataItemTextFromText),
    }
)

excel_msp_driver = ExcelInputFormat({
    'task_name': ('Task_Name', ColumnDataItemTextFromText),
    'visual_flag': ('Visual_Flag', ColumnDataItemBooleanFromYesNo),
    'visual_text': ('Visual_Text', ColumnDataItemTextFromText),
    'swimlane': ('Visual_Swimlane', ColumnDataItemTextFromText),
    'duration': ('Duration(Exp)', ColumnDataItemIntegerFromMspDurationText),
    'start_date': ('Start_Date', ColumnDataItemDateFromMSPString),
    'end_date': ('Finish_Date', ColumnDataItemDateFromMSPString),
    'num_track_within_swimlane': ('Visual_Track_Num_Within_Swimlane', ColumnDataItemIntegerFromText),
    'num_tracks_to_cover': ('Visual_Num_Tracks_To_Cover', ColumnDataItemIntegerFromText),
    'text_layout': ('Text_Layout', ColumnDataItemTextFromText),
    'outstanding_format_name': ('Format_String', ColumnDataItemTextFromText),
    'complete_format_name': ('Done_Format_String', ColumnDataItemTextFromText),
}
)
excel_input_formats = {
    'SmartSheetExport': excel_smartsheet_driver,
    'MSP_Export' : excel_msp_driver,
}
