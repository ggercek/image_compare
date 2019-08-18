# -*- coding: utf-8 -*-

"""Main module."""

import time
import logging
from image_compare.similarity import get_similarity_measurement
from image_compare.exceptions import ICError, FileError, ArgumentError
from image_compare.file_handlers import FileHandlerFactory


log_levels = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}


class ExitCodes:
    ARGUMENT_ERROR = 10
    FILE_ERROR = 11
    UNKNOWN_ERROR = 90


def __real_main(config):
    time_start = time.process_time()
    time_end = 0
    try:
        input_handler = None
        output_handler = None
        similarity = None
        pairs = None
        num_of_pairs = 0
        headers = ["image1", "image2", "similarity", "elapsed"]

        # Init file handlers
        try:
            input_handler = FileHandlerFactory().getInputHandler(filename=config.input_file)
            output_handler = FileHandlerFactory().getOutputHandler(filename=config.output_file, headers=headers)
        except FileError as fe:
            logging.error("Error occurred while creating file handlers: {fe}", fe)
            return ExitCodes.FILE_ERROR

        # Init similarity
        try:
            similarity = get_similarity_measurement(config.distance)
        except ArgumentError as ae:
            logging.error(ae.message)
            return ExitCodes.ARGUMENT_ERROR

        # Parse input file
        try:
            logging.info(f"Parsing file {config.input_file}")
            input_handler.read()
            pairs = input_handler.records
            logging.info(f"Successfully parsed. {len(pairs)} pair(s)")
        except FileError as fe:
            logging.error(f"Error occured while parsing input file. {fe}")
            return ExitCodes.FILE_ERROR

        # Calculate similarity between images and update pair object
        num_of_pairs = len(pairs)
        for pair in pairs:
            if pair.skipped is False:
                try:
                    similarity(pair)
                    logging.info(f"Processed: {pair.line_num:03d}/{num_of_pairs:03d} - "
                                 f"similarity:{pair.similarity:.4f}\telapsed:{pair.elapsed:.5f}")
                except ICError as e:
                    logging.warning(f"Skipping line number:{pair.line_num}, "
                                    f"error occured while calculating similarity> {e}")
            else:
                logging.warning(f"Skipping line number:{pair.line_num}")

        # Write pairs to file
        try:
            logging.info(f"Writing pairs to {config.output_file} with overwrite={config.overwrite_output}")
            output_handler.write(pairs, config.overwrite_output)
            logging.info(f"Successfully saved {len(pairs)} pair(s).")
        except FileError as fe:
            # In case of an error write results to log file
            logging.error(f"Error occured while writing to output file {fe}")
            logging.error("To keep the results, pairs will be dumped here")
            logging.error('\n'+'\n'.join([str(p) for p in pairs]))
            return ExitCodes.FILE_ERROR

        # Generate a execution summary
        time_end = time.process_time()
        num_of_skipped_pairs = sum([pair for pair in pairs if pair.skipped])

        logging.info(f"Summary: "
                     f"\n\tInput: {config.input_file}"
                     f"\n\tOutput: {config.output_file}"
                     f"\n\tProcessed: {num_of_pairs}"
                     f"\n\tSkipped: {num_of_skipped_pairs}"
                     f"\n\tUsed Distance:{config.distance}"
                     f"\n\tTotal time:{time_end - time_start} seconds")

    except Exception as e:
        # Catch all statement in case we missed something
        logging.exception(f"Unhandled exception occurred, exiting...\n {e}")
        return ExitCodes.UNKNOWN_ERROR

    return 0


def main(config):
    """Main function"""

    logging.basicConfig(filename=config.log_filename, filemode='a', level=log_levels[config.log_level],
                        format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")

    if not config.quiet:
        console = logging.StreamHandler()
        console.setLevel(config.log_level)
        logging.getLogger('').addHandler(console)

    logging.info(f"Starting with {config}")
    exit_value = __real_main(config)
    logging.info(f"Ending with exit value: {exit_value}")
    return exit_value
