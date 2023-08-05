import click
import json
from .runs import commands as runs_commands
from .run import commands as run_commands
from ..utils import get_client, handle_error_gracefully


@click.group("wes")
def wes():
    pass


@wes.command("info")
@click.pass_context
@handle_error_gracefully
def get_service_info(ctx):
    click.echo(
        json.dumps(
            get_client(ctx).wes.info(),
            indent=4,
        )
    )


wes.add_command(runs_commands.runs)
wes.add_command(run_commands.run)
