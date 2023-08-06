from pathlib import Path
import sys
from typing import Optional

from simple_term_menu import TerminalMenu
import typer

from .core import (
    AnimationDetail,
    Character,
    RawDetail,
    UMIGAP
)


def create_project(slug: str, title: str, target: str):
    """ Create a yaml for a umigap project """
    obj = UMIGAP(slug=slug, name=title, target=target)

    project_path = Path(slug)
    if not project_path.exists():
        project_path.mkdir()

    for i in ["raw", "ready_to_rig", "rigged", "final"]:
        path = (project_path / Path(i))
        if not path.exists():
            path.mkdir(exist_ok=True)

    if obj.get_save_path().exists():
        typer.echo(f"Configuration file for {slug} already exists.")

    obj.add_tool("blender", stages=["import"])
    obj.add_tool("auto-rig-pro-autorig", stages=["rig"])
    obj.add_tool("auto-rig-pro-bvh", stages=["animation"])
    obj.add_tool("preception-neuron", stages=["mocap"])

    obj.stages = [
        "import",
        "mocap",
        "rig",
        "animation",
        "publish"
    ]
    obj.save()
    return obj


def cli_selector(slug: Optional[str] = None, options=None, title="Select"):
    """ Find a mocap """
    slug = slug.lower() if slug else ""
    options = [] if not options else options

    if not slug:
        terminal_menu = TerminalMenu(options, title=title)
        menu_entry_index = terminal_menu.show()
        slug = options[menu_entry_index]

    return slug


def cli_character_selector(obj: UMIGAP, character_slug: Optional[str] = None):
    """ Find a character """
    return cli_selector(character_slug, list(obj.characters.keys()), "Select character")


def cli_mocap_selector(obj: UMIGAP, mocap_slug: Optional[str] = None):
    """ Find a mocap """
    return cli_selector(mocap_slug, list(obj.mocaps.keys()), "Select mocap")


def add_character(slug: str, character_slug: str, file_path: str):
    """ Add a character to the project """
    typer.echo("adding character")
    if not character_slug:
        character_slug = input("character slug >")
    obj = UMIGAP.load(slug)
    character = Character(character_slug)
    character_slug = character_slug.lower()
    output = Path("ready_to_rig") / Path(character_slug)
    output.mkdir(parents=True, exist_ok=True)
    output_file = (output / Path(character_slug).with_suffix(".blend")).as_posix()
    raw_detail = RawDetail(input=file_path, output=output_file)
    character.raw = raw_detail

    obj.characters[character_slug] = character
    obj.save()
    typer.echo(f"Added character {character_slug} to {slug}.")


def add_mocap(slug: str, mocap_slug: str):
    typer.echo("adding mocap")
    if not mocap_slug:
        mocap_slug = input("mocap slug >")
    obj = UMIGAP.load(slug)
    obj.add_mocap(mocap_slug)
    obj.save()
    typer.echo(f"Added mocap {mocap_slug} to {slug}.")


def add_tool(slug: str, instruction_slug: str):
    typer.echo("adding tool")
    if not instruction_slug:
        instruction_slug = input("tool slug >")
    obj = UMIGAP.load(slug)

    obj.add_tool(instruction_slug)
    obj.save()
    typer.echo(f"Added tool {instruction_slug} to {slug}.")


# character tools
def import_character_from_raw(slug: str, character_slug: str):
    """ Apply the stored transformations to the raw art asset """
    typer.echo("import raw art for character")

    obj = UMIGAP.load(slug)
    character_slug = cli_character_selector(obj, character_slug)

    character = obj.characters[character_slug]
    variation = character.variations.get("default")
    if not variation:
        sys.exit(f"Not enough details about {character_slug} to import")
    typer.echo(f"TODO: import {character_slug} to {variation.output}")


def connect_character_mocap(slug: str, character_slug: str, mocap_slug: str):
    """ Create an animation entry for the character using the requested mocap """
    obj = UMIGAP.load(slug)

    character_slug = cli_character_selector(obj, character_slug)
    mocap_slug = cli_mocap_selector(obj, mocap_slug)

    if character_slug not in obj.characters:
        sys.exit(f"{character_slug} not found in project characters.")

    if mocap_slug not in obj.mocaps:
        sys.exit(f"{mocap_slug} not found in project mocap datasets.")

    character = obj.characters[character_slug]
    mocap = obj.mocaps[mocap_slug]

    detail = AnimationDetail(mocap=mocap_slug, description=mocap.description)

    character.animations[f"{character_slug}_{mocap_slug}"] = detail
    obj.save()
    typer.echo(f"Connected {mocap_slug} to {character_slug}.")

