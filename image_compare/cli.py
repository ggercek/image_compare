# -*- coding: utf-8 -*-

"""Console script for image_compare."""
import sys
import click


@click.command()
def main(args=None):
    """Console script for image_compare."""
    click.echo("Replace this message by putting your code into "
               "image_compare.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
