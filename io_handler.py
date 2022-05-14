import pandas


class CSVReader:
    def __init__(self, input_file):
        self.input_file = input_file
        self.data = self.__read()

    def __read(self):
        return pandas.read_csv(self.input_file)

    def readISBN(self):
        """Yields each row of dataframe one by one."""
        isbn_column = "ASIN"
        data_size = len(self.data[isbn_column])
        for i in range(0, data_size):
            row = self.data.iloc[i]
            yield row[isbn_column]

class XLSXReader(CSVReader):
    def __init__(self, input_file):
        self.input_file = input_file
        self.data = self.__read()

    def __read(self):
        return pandas.read_excel(self.input_file)

class CSVWriter:
    def __init__(self, input_file):
        self.input_file = input_file
        self.buffer = {}

    def set_columns(self, columns):
        for col in columns:
            self.buffer[col] = []

    def add_to_buffer(self, row):
        for col in row.keys():
            self.buffer[col].append(row[col])

    def write(self):
        pandas.DataFrame(self.buffer).to_csv(self.input_file, index=False)

class XLSXWriter:
    def __init__(self, input_file):
        super().__init__(input_file)

    def write(self):
        pandas.DataFrame(self.buffer).to_excel(self.input_file, index=False)
