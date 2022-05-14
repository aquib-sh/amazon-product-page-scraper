import config
from io_handler import CSVReader, CSVWriter, XLSXReader, XLSXWriter
from scraper import ProductScraper


class App:
    def __init__(self):
        self.scraper = ProductScraper()
        self.reader = self.__create_reader(config.INPUT_FILE)
        self.writer = self.__create_writer()

    def __create_reader(self, input_file):
        if input_file.endswith("csv"):
            return CSVReader(input_file)
        elif input_file.endswith("xlsx"):
            return XLSXReader(input_file)

        raise Exception(f"Invalid File Format: {input_file}")

    def __create_writer(self, output_file):
        if output_file.endswith("csv"):
            return CSVWriter(output_file)
        elif output_file.endswith("xlsx"):
            return XLSXWriter(output_file)

        raise Exception(f"Invalid File Format: {output_file}")

    def run(self):
        i = 0
        for isbn in self.reader.readISBN():
            info = self.scraper.scrape(isbn)

            if not i: 
                self.writer.set_columns(list(info.keys()))
                i = not i

            self.writer.add_to_buffer(info)
        self.writer.write()
