import os
import json
import click
import warnings


@click.command()
@click.argument(
    "path",
    nargs=-1,
    type=click.Path(
        exists=True, file_okay=True, dir_okay=True, readable=True, allow_dash=True
    ),
    is_eager=True,
)
def main(path):
    for fname in path:
        if os.path.isfile(fname):
            if not fname.endswith(".json"):
                raise Exception("Please pass valid JSON files")
            format(fname)
        elif fname == ".":
            formatted = [format(i) for i in get_nested_files(os.getcwd())]
            count_true = formatted.count(True)
            print(
                f"{'No' if count_true == 0 else count_true} JSON {'file' if count_true == 0 else 'files'} formatted"
            )
        elif os.path.isdir(fname):
            formatted = [format(i) for i in get_nested_files(fname)]
            print(
                f"{'No' if count_true == 0 else count_true} JSON {'file' if count_true <=1 else 'files'} formatted"
            )


def format(fname):
    try:
        with open(fname, "r") as f:
            json_data = json.load(f)
        with open(fname, "w") as f:
            json.dump(json_data, f, indent=4, sort_keys=True)
        print(f"Formatted :: {fname}")
        return True
    except:
        warning = f"Unable to format file {fname}"
        warnings.warn(warning)
        return False


def get_nested_files(fname):
    json_files = []
    for path, subdirs, files in os.walk(fname):
        for name in files:
            file = os.path.join(path, name)
            if file.endswith(".json"):
                json_files.append(file)
    return json_files
