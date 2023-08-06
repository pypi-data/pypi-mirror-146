import click

from tecton.cli.command import TectonGroup
from tecton_spark import conf


# TODO(snowflake): Unhide
@click.command(cls=TectonGroup, hidden=True)
def snowflake():
    """Snowflake-related commands."""


@snowflake.command(requires_auth=False)
def configure():
    conf.set("ALPHA_SNOWFLAKE_COMPUTE_ENABLED", "true")
    conf.save_tecton_configs()
