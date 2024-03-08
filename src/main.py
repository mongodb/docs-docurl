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
@click.option('--file', '-f', default='assets.toml',
              help='Use a specific assets file',
              show_default=True)
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
@click.option('--file', '-f', default='assets.toml',
              help='Use a specific assets file',
              show_default=True)
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
@click.option('--file', '-f', default='assets.toml',
              help='Use a specific assets file',
              show_default=True)
def fetch(ctx, file):
    """
    Fetch all assets.
    """
    g = ctx.obj["G"]
    assets = read_assets_file(file)
    download_assets(assets, g)


@docurl.command()
@click.pass_context
@click.option('--file', '-f', default='assets.toml',
              help='Use a specific assets file',
              show_default=True)
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
