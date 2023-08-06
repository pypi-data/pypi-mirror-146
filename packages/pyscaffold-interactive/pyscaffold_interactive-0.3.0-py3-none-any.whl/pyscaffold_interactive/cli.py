# -*- coding: utf-8 -*-
"""
Interactively generate a Python project template with customizations
using PyScaffold
"""

import click
import shutil
import subprocess
import sys
from collections.abc import Iterable
from pyscaffold import templates

__author__ = "Sarthak Jariwala"
__copyright__ = "Sarthak Jariwala"
__license__ = "mit"


def prompt_text(text, default=None):
    """Prompt user text input"""
    prompt_ans = click.prompt(click.style(text, fg="blue"), default=default)
    return prompt_ans


def prompt_choice(text, choices, default=None):
    """Prompt user input from provided choices"""
    # choices must be iterable
    assert isinstance(choices, Iterable)

    prompt_ans = click.prompt(
        click.style(text, fg="blue"),
        show_choices=True,
        type=click.Choice(choices, case_sensitive=False),
        default=default,
    )

    return prompt_ans


@click.command()
def main():
    """Interactive Python/DataScience project template setup using PyScaffold"""

    license_choices = templates.licenses.keys()

    if sys.platform == "win32":
        cmds = ["cmd", "/c", shutil.which("putup")]
    else:
        cmds = ["putup"]

    click.echo(
        click.style(
            "\nPyScaffold-Interactive - A tool to interactively "
            + "create python project templates using PyScaffold\n",
            fg="green",
        )
    )

    project_name = prompt_text("Enter your project name ", default="PyProject")
    cmds.append(f"{project_name}")

    description = prompt_text(
        "Enter short description",
        default="Generated using PyScaffold-Interactive",
    )
    cmds.append(f"-d {description}")

    url = prompt_text(
        "Project URL",
        default="https://github.com/SarthakJariwala/PyScaffold-Interactive",
    )
    cmds.append(f"-u {url}")

    is_data_sci_proj = prompt_choice(
        "Is this a DataScience project?", ["y", "n"], default="n"
    ).lower()

    if is_data_sci_proj == "y":
        cmds.append("--dsproject")

    create_ci = prompt_choice(
        "Do you want to use GitHub Actions or GitLab CI? ",
        ["GitHub", "GitLab", "None"],
        default="GitHub",
    ).lower()

    if create_ci == "github":
        cmds.append("--github")
    elif create_ci == "gitlab":
        cmds.append("--gitlab")

    # only ask for pre-commit if not datascience project, auto-yes for datasci project
    if is_data_sci_proj == "n":
        create_pre_commit = prompt_choice(
            "Generate pre-commit config? [Recommended] ", ["y", "n"], default="y"
        ).lower()

        if create_pre_commit == "y":
            cmds.append("--pre-commit")

    # only ask for markdown if not datascience project, auto-yes for datasci project
    if is_data_sci_proj == "n":
        create_markdown = prompt_choice(
            "Use Markdown or Restructured Text for documentation?",
            ["md", "rst"],
            default="md",
        ).lower()

        if create_markdown == "md":
            cmds.append("--markdown")

    license = prompt_choice("Choose License", license_choices, default="mit").lower()
    cmds.append(f"-l {license}")

    click.echo(click.style("\nSetting up your project...", fg="green"))
    # setup datascience project using putup
    subprocess.call(cmds)

    click.echo(
        click.style(f"\nSuccess! {project_name} created. Lets code!", fg="green")
    )

    click.echo(
        click.style(
            "\nAll pyscaffold commands are also available. For help - ", fg="green"
        )
        + click.style("'putup --help'", fg="blue")
    )


def run():
    """Entry point for console_scripts"""
    main()


if __name__ == "__main__":
    run()
