"""Console script for kzr_snowflake."""
import sys
import click


@click.command()
def main(args=None):
    """Console script for kzr_snowflake."""
    click.echo("See click documentation at https://github.com/kzraryan-mu/kzr_libs")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
