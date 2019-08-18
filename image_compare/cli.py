# -*- coding: utf-8 -*-

"""Console script for image_compare."""
import sys
import click
from image_compare import image_compare
from image_compare.models import Config
from image_compare.similarity import get_supported_similarity_methods


@click.command()
@click.argument("input_file")
@click.argument("output_file")
@click.option("--overwrite-output", is_flag=True, default=False, show_default=True,
              help="Overwrite the output if already exists")
@click.option("--quiet", is_flag=True, default=False, show_default=True,
              help="Suppress console output")
@click.option("--distance", type=click.Choice(get_supported_similarity_methods()), default="ssim", show_default=True,
              help="Similarity method to compare image pairs")
@click.option("--log-level", type=click.Choice(image_compare.log_levels.keys()), default="INFO", show_default=True,
              help="Log level to control the output volume")
@click.option("--log-filename", default="image_compare.log", show_default=True,
              help="Log file path")
def main(input_file, output_file, overwrite_output, quiet, distance, log_level, log_filename):
    """A tool to compare given image pairs

        Sample Commands:

        # use default options

        image_compare files/product-cat-photos.csv files/product-cat-photos.csv

        # use dhash

        image_compare --distance=dhash files/product-cat-photos.csv files/product-cat-photos.csv

        # use whash and overwrite output

        image_compare --distance=whash --overwrite-output files/product-cat-photos.csv files/product-cat-photos.csv

        # use ssim and use my_log_file.log as logging, and no console output

        image_compare --distance=ssim --log-filename="my_log_file.log" --quiet files/product-cat-photos.csv files/product-cat-photos.csv

    """
    config = Config(input_file, output_file, overwrite_output, quiet, distance, log_level, log_filename)
    return image_compare.main(config)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
