import os
from typing import List

import click

from ..utils import get_client, handle_error_gracefully


@click.group()
def files():
    pass


@files.command("download")
@click.pass_context
@click.argument("urls", required=False, nargs=-1)
@click.option(
    "-o", "--output-dir", required=False, default=os.getcwd(), show_default=True
)
@click.option("-i", "--input-file", required=False, default=None)
@click.option("-q", "--quiet", is_flag=True, required=False, default=False)
@handle_error_gracefully
def download(
    ctx: click.Context,
    urls: List[str],
    output_dir: str = os.getcwd(),
    input_file: str = None,
    quiet: bool = False,
):
    download_urls = []

    if len(urls) > 0:
        download_urls = list(urls)
    elif input_file:
        with open(input_file, "r") as infile:
            download_urls = filter(
                None, infile.read().split("\n")
            )  # need to filter out invalid values
    else:
        if not quiet:
            click.echo("Enter one or more URLs. Press q to quit")

        while True:
            try:
                url = click.prompt("", prompt_suffix="", type=str)
                url = url.strip()
                if url[0] == "q" or len(url) == 0:
                    break
            except click.Abort:
                break

            download_urls.append(url)
    get_client(ctx).download(
        urls=download_urls, output_dir=output_dir, display_progress_bar=(not quiet)
    )
