#!/usr/bin/env python

import re
import subprocess
from pathlib import Path

import click


@click.command()
@click.argument("new_version")
def main(new_version: str) -> None:
    """
    This script takes care of what is needed to prepare a new version of the
    package.

    It does the following steps:
    - create new branch
    - update `magika.__init__.__version__` with `new_version`
    - update `Unreleased` => `new_version` in `CHANGELOG.md` + add date
    - git commit
    - print next steps

    If the new version ends -dev, we just update the version in the main repo
    and we don't create tags.
    """

    python_root_dir = Path(__file__).parent.parent / "python"
    current_version = get_python_version(python_root_dir)

    patch_python_version(python_root_dir, new_version)
    patch_changelog_version(python_root_dir, new_version)

    print(f"Version updated successfully: {current_version} => {new_version}")

    click.confirm(
        "Check the git diff of the main repo; is it good to go?",
        default=True,
        abort=True,
    )

    print("Committing and tagging to main repo")

    magika_init_path = python_root_dir / "src" / "magika" / "__init__.py"
    changelog_path = python_root_dir / "CHANGELOG.md"

    # create new branch
    cmd = ["git", "checkout", "-b", f"python-new-release-{new_version}"]
    print(f"Executing: {cmd}")
    subprocess.run(cmd, check=True)

    # git add + commit these changes
    cmd = ["git", "add", str(magika_init_path), str(changelog_path)]
    print(f"Executing: {cmd}")
    subprocess.run(cmd, check=True)
    cmd = ["git", "commit", "-m", f'Update to version "{new_version}"']
    print(f"Executing: {cmd}")
    subprocess.run(cmd, check=True)

    # add tag
    # cmd = ["git", "tag", f"python-v{new_version}"]
    # print(f"Executing: {cmd}")
    # subprocess.run(cmd, check=True)

    print(
        "Everything went fine! Next steps: push this branch, create a PR, merge it, and then tag it."
    )


def get_python_version(python_root_dir: Path) -> str:
    init_path = python_root_dir / "src" / "magika" / "__init__.py"
    version = extract_with_regex(init_path, '__version__ = "([A-Za-z0-9.-]+)"')
    print(f"Extracted python version: {version}")
    return version


def patch_python_version(python_root_dir: Path, new_version: str):
    # TODO: patch it
    assert get_python_version(python_root_dir) == new_version


def patch_changelog_version(python_root_dir: Path, new_version: str):
    pass


def extract_with_regex(file_path: Path, regex: str) -> str:
    """Extract a string via regex. This raises an exception if no or more than
    one matches are found."""

    lines = file_path.read_text().split("\n")
    output = None
    for line in lines:
        m = re.fullmatch(regex, line)
        if m:
            if output is not None:
                raise Exception(
                    f'ERROR: Found more than one match for "{regex}" in {file_path}'
                )
            output = m.group(1)
    if output is None:
        raise Exception(f'No hits for "{regex}" in {file_path}')
    return output


if __name__ == "__main__":
    main()
