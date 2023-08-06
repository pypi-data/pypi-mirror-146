import sys
import warnings
from pathlib import Path
from typing import List, Optional

import typer
from simple_term_menu import TerminalMenu

from .core import (
    UMIGAP,
    AnimationConnection,
    Character,
    Mocap,
    RawDetail,
    RigDetail,
    Tool,
)


def create_project(slug: str, title: str, target: str):
    """Create a yaml for a umigap project"""
    obj = UMIGAP(slug=slug, name=title, target=target)

    project_path = Path(slug)
    if not project_path.exists():
        project_path.mkdir()

    for i in ["raw", "ready_to_rig", "rigged", "final", "plugins"]:
        path = project_path / Path(i)
        if not path.exists():
            path.mkdir(exist_ok=True)

    if obj.get_save_path().exists():
        typer.echo(f"Configuration file for {slug} already exists.")

    obj.add_tool("blender", Tool(stage="import"))
    obj.add_tool("auto-rig-pro-autorig", Tool(stage="rig"))
    obj.add_tool("auto-rig-pro-bvh", Tool(stage="animation"))
    obj.add_tool("preception-neuron", Tool(stage="mocap"))

    obj.stages = ["import", "mocap", "rig", "animation", "publish"]
    obj.save()
    return obj


def cli_selector(slug: Optional[str] = None, options=None, title="Select"):
    """Select a single item"""
    slug = slug.lower() if slug else ""
    options = [] if not options else options

    if not slug:
        terminal_menu = TerminalMenu(options, title=title)
        menu_entry_index = terminal_menu.show()
        slug = options[menu_entry_index]

    return slug


def cli_character_selector(obj: UMIGAP, character_slug: Optional[str] = None):
    """Find a character"""
    return cli_selector(character_slug, list(obj.characters.keys()), "Select character")


def cli_mocap_selector(obj: UMIGAP, mocap_slug: Optional[str] = None):
    """Find a mocap"""
    return cli_selector(mocap_slug, list(obj.mocaps.keys()), "Select mocap")


def cli_stage_selector(obj: UMIGAP, stage_slug: Optional[str] = None):
    """Select stages"""
    return cli_selector(stage_slug, list(obj.tools.keys()), "Select stage")


def cli_animation_selector(obj: UMIGAP, character_slug: str):
    """Select stages"""
    options = obj.find_character(character_slug).animations
    return cli_selector(None, options, "Select animation")


def add_character(slug: str, character_slug: str, file_path: str):
    """Add a character to the project"""
    typer.echo("adding character")
    if not character_slug:
        character_slug = input("character slug >")
    obj = UMIGAP.load(slug)
    character = Character(character_slug)
    character.input = file_path

    character_slug = character_slug.lower()
    obj.add_character(character_slug, character)

    obj.save()
    typer.echo(f"Added character {character_slug} to {slug}.")


def add_mocap(slug: str, mocap_slug: str, file_path: str):
    typer.echo("adding mocap")
    if not mocap_slug:
        mocap_slug = input("mocap slug >")
    obj = UMIGAP.load(slug)
    name = f"{mocap_slug.title()} Mocap"
    obj.add_mocap(mocap_slug, Mocap(name, input=file_path))
    obj.save()
    typer.echo(f"Added mocap {mocap_slug} to {slug}.")


def add_tool(slug: str, instruction_slug: str):
    typer.echo("adding tool")
    if not instruction_slug:
        instruction_slug = input("tool slug >")
    obj = UMIGAP.load(slug)
    stage_slug = cli_stage_selector(obj)

    obj.add_tool(instruction_slug, Tool(stage=stage_slug))
    obj.save()
    typer.echo(f"Added tool {instruction_slug} to {slug}.")


# character tools
def import_character_from_raw(slug: str, character_slug: str):
    """Apply the stored transformations to the raw art asset"""
    typer.echo("import raw art for character")

    obj = UMIGAP.load(slug)
    character_slug = cli_character_selector(obj, character_slug)

    # character = obj.characters[character_slug]
    typer.echo(f"TODO: import and transform {character_slug} raw asset")


def connect_character_mocap(slug: str, character_slug: str, mocap_slug: str):
    """Create an animation entry for the character using the requested mocap"""
    obj = UMIGAP.load(slug)

    character_slug = cli_character_selector(obj, character_slug)
    mocap_slug = cli_mocap_selector(obj, mocap_slug)

    if character_slug not in obj.characters:
        sys.exit(f"{character_slug} not found in project characters.")

    if mocap_slug not in obj.mocaps:
        sys.exit(f"{mocap_slug} not found in project mocap datasets.")

    mocap = obj.mocaps[mocap_slug]

    key = f"{character_slug}_{mocap_slug}"

    detail = AnimationConnection(mocap=mocap_slug, description=mocap.description)

    obj.add_animation(key, detail, character_slug)

    obj.save()
    typer.echo(f"Connected {mocap_slug} to {character_slug}.")


def rig_character(slug: str, character_slug: str):
    obj = UMIGAP.load(slug)
    character_slug = cli_character_selector(obj, character_slug)

    rig_slug = f"{character_slug}_rig"

    tool = obj.find_tool_for_stage("rig")
    obj.add_rig(rig_slug, RigDetail(tool=tool), character_slug)

    obj.save()

    typer.echo(f"TODO: autorig {character_slug} for {slug}")


def animate_character(slug: str, character_slug: str, animation_slug: str):
    typer.echo(
        f"Applying mocap {animation_slug} to rigged character {character_slug} in {slug}."
    )

    obj = UMIGAP.load(slug)

    if not animation_slug:
        character_slug = cli_character_selector(obj, character_slug)
        animation_slug = cli_animation_selector(
            obj, character_slug
        )  # select from a character

    # TODO filter on tool
    warnings.warn(
        "umigap currently ignores settings and force uses auto-rig-pro-bvh plugin to apply mocap."
    )
    plugin_apply_mocap_auto_rig_pro_bvh(obj, character_slug, animation_slug)


# mocap tools


def import_mocap_from_raw(slug: str, mocap_slug: str):
    typer.echo("import raw mocap data for pipeline")

    obj = UMIGAP.load(slug)
    mocap_slug = cli_mocap_selector(obj, mocap_slug)
    typer.echo(f"TODO: import {mocap_slug} to {slug}")


# publish tools


def publish_animations(
    slug: str, character_slug: str, animation_slug: str, tag: str, force_all=False
):

    obj = UMIGAP.load(slug)
    if force_all:
        animations = [x[0] for x in obj.animations.items() if x[1].draft is not True]
    elif animation_slug in obj.animations:
        animations = [animation_slug]
    else:
        character_slug = cli_character_selector(obj, character_slug)
        animations = [
            cli_animation_selector(obj, character_slug)
        ]  # select from a character

    tool = obj.find_tool_for_stage("publish")
    print(f"Will publish f{animations} using {tool}")


# plugins -- actually manipulate data
def plugin_apply_mocap_auto_rig_pro_bvh(
    obj: UMIGAP, character_slug: str, mocap_slug: str
):
    """
    Use auto-rig-pro and blender to apply bvh data to a model
    """
    # use blender.apply_mocap_character
    typer.echo("TODO: apply mocap data to model.")
