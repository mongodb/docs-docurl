import click

from src.manage_examples import (
    check_assets,
    read_assets_file,
    download_assets,
    update_repos,
    get_gh_client,
)

@click.group()
@click.pass_context
def docurl(ctx):
    g = get_gh_client()
    ctx.ensure_object(dict)
    ctx.obj["G"] = g

@docurl.command()
@click.pass_context
@click.option('--file', prompt='Assets file',
              help='Relative path of an assets.toml file (optional)')
def outdated(ctx, file):
    """
    List any outdated assets from `repository` entries.
    """
    g = ctx.obj["G"]
    assets = read_assets_file(file)
    outdated = check_assets(assets, g)
    click.echo(outdated)


@docurl.command()
@click.pass_context
@click.option('--file', prompt='Assets file',
              help='Relative path of an assets.toml file (optional)')
def update(ctx, file):
    """
    Update assets. This doesn't download assets by itself.
    """
    g = ctx.obj["G"]
    assets = read_assets_file(file)
    outdated = check_assets(assets, g)
    update_repos(outdated, assets)


@docurl.command()
@click.pass_context
@click.option('--file', prompt='Assets file',
              help='Relative path of an assets.toml file (optional)')
def fetch(ctx, file):
    """
    Fetch all assets.
    """
    g = ctx.obj["G"]
    assets = read_assets_file(file)
    download_assets(assets, g)


@docurl.command()
@click.pass_context
@click.option('--file', prompt='Assets file',
              help='Relative path of an assets.toml file (optional)')
def carryme(ctx, file):
    """
    Run docurl, end to end. This will update
    versioned asset versions, and fetch all assets.
    """
    g = ctx.obj["G"]
    assets = read_assets_file(file)
    outdated = check_assets(assets, g)
    update_repos(outdated, assets)
    download_assets(assets, g)


if __name__ == "__main__":
    docurl()
