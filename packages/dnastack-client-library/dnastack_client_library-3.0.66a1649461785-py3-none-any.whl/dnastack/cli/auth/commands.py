from typing import Optional

from requests import Request
from time import sleep

import click

from ..utils import get_client, handle_error_gracefully
from ...auth import OAuthTokenAuth
from ...auth.session_store import UnknownSessionError
from ...client.base_client import BaseServiceClient
from ...exceptions import (
    LoginException,
    ServiceTypeNotFoundError
)


@click.group("auth")
def auth():
    pass


def _get_client(ctx: click.Context, adapter_type: str) -> BaseServiceClient:
    client = get_client(ctx)

    service_to_authorize: Optional[BaseServiceClient] = None

    if adapter_type == "data_connect":
        service_to_authorize = client.data_connect
    elif adapter_type == "collections":
        service_to_authorize = client.collections
    elif adapter_type == "wes":
        service_to_authorize = client.wes
    else:
        raise ServiceTypeNotFoundError(adapter_type)

    if not service_to_authorize:
        raise LoginException(msg="There is no configured service")
    elif not service_to_authorize.auth:
        raise LoginException(msg="The authentication information is not defined")

    return service_to_authorize


@auth.command("login")
@click.argument("service")
@click.option("--delay-init", type=int, required=False, default=0, help='Delay the authentication by seconds')
@click.option("--revoke-existing", is_flag=True, default=False, help='If used, the existing session will be automatically revoked before the re-authentication')
@click.pass_context
@handle_error_gracefully
def cli_login(ctx: click.Context, service: str, delay_init: int, revoke_existing: bool):
    click.secho('You do not need to initiate the authentication process manually as it will be done automatically '
                'whenever needed, e.g., first request, session expired, etc.',
                fg='black',
                bg='yellow')

    if delay_init > 0:
        sleep(delay_init)

    service_to_authorize = _get_client(ctx, service)

    authorizer: OAuthTokenAuth = service_to_authorize.auth

    if revoke_existing:
        authorizer.revoke_session()

    # Initiate the authorization flow.
    authorizer(Request())
    click.secho("Login successful", fg="green")

