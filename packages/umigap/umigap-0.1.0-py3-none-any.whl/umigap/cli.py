"""

        activist:
        name: activist
        raw:
        file: Activist / Activist.fbx
        scale: 8.5134
        rotate:
        x: 0
        y: 0
        z: 180
        translate:  # in metres
        x: 0
        y: 0
        z: 0.1935
        decimate:
        default: 0.07
        Activist_R2_Extractor_FBX: 0.01
        _HIgh___export: 0.2
        drop - pivot: true
        volume - pivot:
        - Left_Eye
        - Right_Eye

        importers:
  default:
    description:  Just copy a single file (eg glb) direct, no changes.

characters:


stages:
  import:
    - import
  rig:
    - rig
  mocap:
    - mocap
  animation:
    - animation
  publish:
    - publish
  all:
    - import
    - rig
    - mocap
    - animation
    - publish
"""


from pathlib import Path
import shutil
import sys
from typing import Optional

from simple_term_menu import TerminalMenu
import typer

from .core import (
    UMIGAP,
    Character,
    RawDetail,
    AnimationDetail,
)

app = typer.Typer()

character_app = typer.Typer()
app.add_typer(character_app, name="character")
mocap_app = typer.Typer()
app.add_typer(mocap_app, name="mocap")
tool_app = typer.Typer()
app.add_typer(tool_app, name="tool")


def create_project(slug: str, title: str, target: str):
    project_path = Path(slug)
    #if project_path.exists():
    #    sys.exit(f"Project directory {slug} already exists.")
    project_path.mkdir(exist_ok=True)
    (project_path / Path("raw")).mkdir(exist_ok=True)
    (project_path / Path("ready_to_rig")).mkdir(exist_ok=True)
    (project_path / Path("rigged")).mkdir(exist_ok=True)
    (project_path / Path("final")).mkdir(exist_ok=True)
    obj = UMIGAP(slug=slug, name=title, target=target)
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


def add_character(slug: str, character_slug: str, file_path: str):
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
def import_character(slug: str, character_slug: str):
    character_slug = character_slug.lower()
    typer.echo("adding character")
    if not character_slug:
        character_slug = input("character slug >")
    obj = UMIGAP.load(slug)
    character = obj.characters[character_slug]
    variation = character.variations.get("default")
    if not variation:
        sys.exit(f"Not enough details about {character_slug} to import")
    typer.echo(f"TODO: import {character_slug} to {variation.output}")


@app.command()
def init(slug: Optional[str] = typer.Argument(None)):
    """ Create a new pipeline """
    if not slug:
        slug = input("project slug >")
    if not slug:
        return
    title = "My Game"
    if not title:
        title = input("project title >")
    target = "godot3"
    if not target:
        targets = ["godot3"]
        options = ["[a] godot3"]
        terminal_menu = TerminalMenu(options, title="Target")
        menu_entry_index = terminal_menu.show()
        target = targets[menu_entry_index]
    create_project(slug, title, target)
    typer.echo(f"Created project {slug} targeting {target}.")


# mocap tasks

@mocap_app.command("add")
def mocap_add(
        mocap: str = typer.Option(None),
        project: str = typer.Option(...)):
    """ Add a set of motion capture data to the pipeline """
    add_mocap(project, mocap)


# tool tasks

@tool_app.command("add")
def tool_add(
        tool: str = typer.Option(None),
        project: str = typer.Option(...)):
    """ Add a tool used to generate data in the pipeline """
    add_tool(project, tool)


# character tasks

@character_app.command("add")
def character_add(
        path: str,
        character: str = typer.Option(None),
        project: str = typer.Option(...)):
    """ Add a character to the pipeline for a project """
    add_character(project, character, path)


@character_app.command("import")
def character_import(
        character: str = typer.Option(None),
        project: str = typer.Option(...)):
    """ Import the raw 3D file and transform it. """
    import_character(project, character)


# connecting tasks

@app.command()
def connect(instruction: str, project: str = typer.Option(...)):
    """ Connect a mocap dataset to a character in a project """
    typer.echo(project)


# navigation utilities (eg info, ls, etc)
@app.command()
def characters(project: str = typer.Option(...)):
    """ List all the characters in a project pipeline """
    obj = UMIGAP.load(project)
    for c in obj.characters.keys():
        typer.echo(c)


@app.command()
def mocaps(project: str = typer.Option(...)):
    """ List all the mocap datasets in a project pipeline """
    obj = UMIGAP.load(project)
    for c in obj.mocaps.keys():
        typer.echo(c)


if __name__ == "__main__":
    app()
