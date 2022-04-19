import os
import requests
import tomli
import tomli_w
from github import Github
from py_console import console


def read_assets_file():

    try:
        with open("assets.toml", "rb") as f:
            try:
                assets_toml = tomli.load(f)
            except tomli.TOMLDecodeError as e:
                console.error("Failed to parse assets.toml")
                console.error(e)
                exit(1)
    except FileNotFoundError:
        console.error(
            "No `assets.toml` file found. Please create one. See <this wiki article placeholer> for more information."
        )
        exit(1)

    return assets_toml


def get_gh_client():
    # API token is required to avoid rate-limiting
    api_token = os.environ["GITHUB_API_TOKEN"]
    if api_token is None:
        console.error("Please set the GITHUB_API_TOKEN environment variable.")
        console.warn(
            "See https://github.com/settings/tokens to generate a new token, if needed."
        )
        exit(1)
    g = Github(api_token)
    return g


def check_assets(assets_toml, g):
    out_of_date = False
    outdated = {}
    for asset in assets_toml["assets"]["sources"]["repository"]:
        version = asset.get("version")
        if version is None:
            continue
        repo = asset.get("repo")
        gh_repo = g.get_repo(repo)
        releases = gh_repo.get_releases()
        if releases.totalCount == 0:
            continue
        for release in releases:
            if not release.prerelease and not release.draft:
                latest_tag = release.tag_name
                break
        if latest_tag is not None and version == latest_tag:
            pass
        else:
            outdated.update({repo: latest_tag})
            out_of_date = True

    if not out_of_date:
        console.success("All drivers versions are up to date.")
    else:
        console.warn("Some versions are out of date.")
        console.warn(f"{', '.join([elem for elem in outdated.keys()])}")
    return outdated


def update_repos(outdated, assets_toml):
    for (i, source) in enumerate(assets_toml["assets"]["sources"]["repository"]):
        if source["repo"] in outdated.keys():
            repo = source["repo"]
            version = outdated[repo]
            console.info(f"Updating {repo}@{version}...")
            assets_toml["assets"]["sources"]["repository"][i]["version"] = version
            with open("assets.toml", "wb") as f:
                tomli_w.dump(assets_toml, f)
            console.success(f"{repo} updated to @{version}.")


def download_assets(assets_toml, g):
    fetched = 0

    for source_type in assets_toml["assets"]["sources"]:
        for source in assets_toml["assets"]["sources"][source_type]:
            if source_type == "repository":
                fetched += download_repository_assets(
                    source,
                    assets_toml["assets"]["output_paths"][f"{source_type}_path"],
                    g,
                )
            else:
                fetched += (
                    1
                    if download_other_assets(
                        source,
                        assets_toml["assets"]["output_paths"][f"{source_type}_path"],
                    )
                    else 0
                )
    console.info(f"Fetched {fetched} files.")


def dest_path(dest):
    cwd = os.getcwd()
    return os.path.join(cwd, dest)


def make_repo_resource_uri(repo, version, path):
    return f"https://raw.githubusercontent.com/{repo}/{version}/{path}"


def download_repository_assets(source, dest, g):

    fetched = 0

    repo = source["repo"]
    version = source.get("version", g.get_repo(repo).default_branch)
    outloc = dest_path(dest)
    os.makedirs(outloc, exist_ok=True)
    for target in source["targets"]:
        src = target["source"]
        out = target["output"]

        url = make_repo_resource_uri(repo, version, src)
        fetched += 1 if fetch_asset(outloc, out, url) else 0
    return fetched


def download_other_assets(source, dest):
    outloc = dest_path(dest)
    os.makedirs(outloc, exist_ok=True)
    src = source["source"]
    out = source["output"]

    return fetch_asset(outloc, out, src)


def fetch_asset(outloc, out, url):
    response = requests.get(url)
    if not response.ok:
        console.error(f"Failed to fetch {url}")
        console.error(response.text)
        return False
    else:
        with open(os.path.join(outloc, out), "wb") as f:
            f.write(response.content)
        return True
