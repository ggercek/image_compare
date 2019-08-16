# -*- coding: utf-8 -*-

"""Console script for image_compare."""
import sys
import click
from image_compare import image_compare
from image_compare.models import Config


@click.command()
@click.argument("input_file")
@click.argument("output_file")
@click.option("--overwrite-output", is_flag=True, default=False)
@click.option("--distance", type=click.Choice(["ssim", "nrmse", "mse"]), default="ssim")
@click.option("--log-level", type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]), default="INFO")
def main(input_file, output_file, overwrite_output, distance, log_level):
    """Console script for image_compare."""
#    click.echo("Replace this message by putting your code into "
#               "image_compare.cli.main")
#    click.echo("See click documentation at http://click.pocoo.org/")
    config = Config(input_file, output_file, overwrite_output, distance, log_level)
    return image_compare.main(config)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
