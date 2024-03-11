# DOCURL

This tool is meant to handle management of remote assets that should
be included in source. It was purpose built for the MongoDB Documentation team.

## TLDR
`DOCURL --help`

## What it does
DOCURL will read declared assets of any type and download them. Assets are declared
in an `assets.toml` file.

By default, the script opens the `assets.toml` file in the same directory
as the command is run. To specify a different file, specify the relative
path to it by using `--file` (or `-f`) option as shown in the following example:

```shell
docurl fetch --file relative/path/to/my-assets.toml
```

**Note:** The `source` and `output` paths are always relative to where you
run DOCURL rather than the path to the toml file.

### Repository Asset Type

The repository type is the only special purpose type. It contains information
about a source repository, and is meant to track versions. DOCURL can check if
the version listed is out of date with the latest release version, and auto-update
the version in the assets list.

Here's an example:

```toml
[[assets.sources.repository]]
repo = "mongodb/mongo-cxx-driver"
version = "r3.6.6"
targets = [
    { source = "src/mongocxx/test/transactions.cpp", output = "cpp-transactions.cpp" },
    { source = "examples/mongocxx/with_transaction.cpp", output = "cpp-with-transaction.cpp" },
]
```

DOCURL will check the version above against the release version, and update if
it is outdated and instructed to do so. It will fetch the resources in the targets
array at that tag.

### Source and Output

DOCURL fetches the assets from *source* (after assembling the correct raw GitHub url),
and will output to a file named whatever is in *output*. The directory the file is put
in is declared in the `assets.output_paths` entry:

```toml
[assets.output_paths]
repository_path = "source/driver-examples"
image_path = "source/images"
raw_path = "source/raw"
```

### Other Types
DOCURL supports fetching any arbitrary resource. Add resources to `assets.sources.x`
where x is the resource type that has a corresponding entry in `assets.output_paths`.

These resource types have two keys, `source` and `output` that tell DOCURL
where to fetch the asset and the filename to save it as. Output paths are
calculated on static lookup - an asset of type `assets.sources.x` must have a
corresponding entry in `assets.output_paths` of `x_path`.

```toml
[assets.output_paths]
repository_path = "source/driver-examples"
image_path = "source/images"
raw_path = "source/raw"

[[assets.sources.repository]]
repo = "mongodb/mongo-python-driver"
version = "4.1.1"
targets = [
    { source = "test/test_examples.py", output = "test_examples.py" },
]

[[assets.sources.image]]
source = "https://raw.githubusercontent.com/mongodb/docs-java/master/source/includes/figures/atlas_connection_select_cluster.png"
output = "atlas_connection_select_cluster.png"

[[assets.sources.raw]]
source = "https://raw.githubusercontent.com/mongodb/mongo-cxx-driver/master/src/mongocxx/test/versioned_api.cpp"
output = "cpp-versioned_api.cpp"
```


## Developing

For testing the package locally, run the following commands to set up a `virtualenv`
and install the requirements:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Then, you can run the code by running the following command:

```bash
python -m src.main <commands>
```

## Releasing

Increment the `version` in `setup.py`.

Releases are published automatically when a tag is pushed to GitHub.

```sh
# Set next version number

   export RELEASE=x.x.x

# Create tags

   git commit --allow-empty -m "Release $RELEASE"
   git tag -a $RELEASE -m "Version $RELEASE"

# Push

   git push upstream --tags
```
