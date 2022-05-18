import pandas
import requests


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
        self.columns = None
        self.buffer = {}

    def set_columns(self, columns):
        self.columns = columns
        for col in self.columns:
            self.buffer[col] = []

    def flush_buffer(self):
        self.buffer = {}
        self.set_columns(self.columns)

    def add_to_buffer(self, row):
        for col in row.keys():
            self.buffer[col].append(row[col])

    def write(self, filemode='a'):
        add_header = False
        if filemode ==  'w': 
            add_header = True
        pandas.DataFrame(self.buffer).to_csv(self.input_file, mode=filemode, index=False, header=add_header)

class XLSXWriter:
    def __init__(self, input_file):
        super().__init__(input_file)

    def write(self):
        pandas.DataFrame(self.buffer).to_excel(self.input_file, index=False)

class WebImageWriter:
    """Downloads image from the web URL and writes it to a file"""
    def __init__(self, imageURL):
        self.URL = imageURL

    def write(self, filename) -> bool:
        retry = 0
        max_retries = 3
        while (retry < max_retries):
            try:
                res = requests.get(self.URL, timeout=10)
                break
            except:
                retry += 1
                if (retry == max_retries):
                    return False
                continue

        if res.status_code in (200, 201):
            fp = open(filename, 'wb')
            fp.write(res.content)
            return True
        return False

