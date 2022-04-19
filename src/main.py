from turtle import down
import click
from .manage_examples import (
    check_assets,
    read_assets_file,
    download_assets,
    update_repos,
    get_gh_client,
)


@click.group()
@click.pass_context
def tenzing(ctx):
    g = get_gh_client()
    ctx.ensure_object(dict)
    ctx.obj["G"] = g


@tenzing.command()
@click.pass_context
def outdated(ctx):
    """
    List any outdated assets from `repository` entries.
    """
    g = ctx.obj["G"]
    assets = read_assets_file()
    outdated = check_assets(assets, g)
    click.echo(outdated)


@tenzing.command()
@click.pass_context
def update(ctx):
    """
    Update assets. This doesn't download assets by itself.
    """
    g = ctx.obj["G"]
    assets = read_assets_file()
    outdated = check_assets(assets, g)
    update_repos(outdated, assets)


@tenzing.command()
@click.pass_context
def fetch(ctx):
    """
    Fetch all assets.
    """
    g = ctx.obj["G"]
    assets = read_assets_file()
    download_assets(assets, g)


@tenzing.command()
@click.pass_context
def carryme(ctx):
    """
    Run Tenzing, end to end. This will update
    versioned asset versions, and fetch all assets.
    """
    g = ctx.obj["G"]
    assets = read_assets_file()
    outdated = check_assets(assets, g)
    update_repos(outdated, assets)
    download_assets(assets, g)


if __name__ == "__main__":
    tenzing()
