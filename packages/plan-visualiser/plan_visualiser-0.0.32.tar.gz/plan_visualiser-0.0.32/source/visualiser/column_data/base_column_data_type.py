from abc import ABC, abstractmethod


class BaseColumnDataType(ABC):
    def __init__(self, input_column_value):
        self.input_column_value = input_column_value
        self.stored_column_value = None

    @abstractmethod
    def interpret_column_value(self, input_value):
        pass

    @property
    def value(self):
        if self.stored_column_value is None:
            self.stored_column_value = self.interpret_column_value(self.input_column_value)
        return self.stored_column_value