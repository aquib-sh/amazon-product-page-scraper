import os

import config
from io_handler import (CSVReader, CSVWriter, WebImageWriter, XLSXReader,
                        XLSXWriter)
from log import Logger
from scraper import ProductScraper


class App:
    def __init__(self):
        self.logger = Logger()
        self.scraper = ProductScraper()
        self.reader = self.__create_reader(config.INPUT_FILE)
        self.writer = self.__create_writer(config.OUTPUT_FILE)

    def __create_reader(self, input_file):
        self.logger.info(f"Reading {input_file}")
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
            # NOTE: REMOVE BELOW CONDITION
            STOP_AT = 41
            if i == STOP_AT:
                break

            self.logger.info(f"Scraping for ISBN: {isbn}")
            info = self.scraper.scrape(isbn)

            if info is None:
                self.logger.error(f"No URL found for {isbn}")
                continue
            if not i: 
                self.writer.set_columns(list(info.keys()))

            i += 1

            self.logger.info("Adding to buffer")
            self.writer.add_to_buffer(info)

            # Download images from the web and write them to the folder
            if not os.path.isdir(config.IMAGE_DIR): os.mkdir(config.IMAGE_DIR)
            image_path = os.path.join(config.IMAGE_DIR, isbn) + ".jpg"

            img_writer = WebImageWriter(info["image_url"])
            if img_writer.write(image_path):
                self.logger.info(f"Downloaded image to {image_path}")
            else:
                self.logger.error(f"Failed to download image from {info['image_url']}")

            # Use 'w' (write) mode when .write() is called first time else use 'a' (append) mode
            if i % 20 == 0:
                if i >= 20:
                    self.writer.write(filemode='a')
                    self.writer.flush_buffer()
                else:
                    self.writer.write(filemode='w')
                self.logger.info(f"Saved {i} results to {config.OUTPUT_FILE}")

            print("\n")

        self.writer.write(filemode='a')
        self.logger.info(f"Saved the results to {config.OUTPUT_FILE}")

if __name__ == "__main__":
    App().run()
