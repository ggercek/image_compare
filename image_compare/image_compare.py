# -*- coding: utf-8 -*-

"""Main module."""

import logging
import image_compare.similarity
from image_compare.file_handlers import CSVInputHandler, CSVOutputHandler

def main(config):
    exit_value = 0

    logging.basicConfig(filename='image_compare.log', filemode='w', level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    try:
        logging.info(f"Started with {config}")
        pass
    except Exception as e:
        pass

    logging.info(f"Ending with exit value: {exit_value}")
    return exit_value
