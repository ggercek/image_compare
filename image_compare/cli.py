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
@click.option("--overwrite-output", is_flag=True, default=False)
@click.option("--distance", type=click.Choice(get_supported_similarity_methods()), default="ssim")
@click.option("--log-level", type=click.Choice(image_compare.log_levels.keys()), default="INFO")
def main(input_file, output_file, overwrite_output, distance, log_level):
    """Console script for image_compare."""
#    click.echo("Replace this message by putting your code into "
#               "image_compare.cli.main")
#    click.echo("See click documentation at http://click.pocoo.org/")
    config = Config(input_file, output_file, overwrite_output, distance, log_level)
    return image_compare.main(config)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
