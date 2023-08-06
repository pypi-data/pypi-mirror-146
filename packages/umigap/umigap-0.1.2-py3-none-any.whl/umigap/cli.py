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


from typing import Optional

import typer
from simple_term_menu import TerminalMenu

from .core import UMIGAP
from .utils import (
    add_character,
    add_mocap,
    add_tool,
    animate_character,
    connect_character_mocap,
    create_project,
    import_character_from_raw,
    import_mocap_from_raw,
    publish_animations,
    rig_character,
)

app = typer.Typer()

character_app = typer.Typer()
app.add_typer(character_app, name="character")
mocap_app = typer.Typer()
app.add_typer(mocap_app, name="mocap")
tool_app = typer.Typer()
app.add_typer(tool_app, name="tool")
# publish_app = typer.Typer()
# app.add_typer(publish_app, name="publish")


@app.command()
def init(slug: Optional[str] = typer.Argument(None)):
    """Create a new pipeline"""
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
    path: str, mocap: str = typer.Option(None), project: str = typer.Option(...)
):
    """Add a set of motion capture data to the pipeline"""
    add_mocap(project, mocap, path)


@mocap_app.command("import")
def mocap_import(mocap: str = typer.Option(None), project: str = typer.Option(...)):
    """Import the raw 3D file and transform it."""
    import_mocap_from_raw(project, mocap)
    typer.echo(
        f"Nothing to do for {mocap} on project {project}"
        f"umigap has no tool for processing raw mocap data. "
        f"Use another tool to manually export the data and place it inside mocap_data/."
    )
    # import_mocap_from_raw(project, character)


# tool tasks


@tool_app.command("add")
def tool_add(tool: str = typer.Option(None), project: str = typer.Option(...)):
    """Add a tool used to generate data in the pipeline"""
    add_tool(project, tool)


# character tasks


@character_app.command("add")
def character_add(
    path: str, character: str = typer.Option(None), project: str = typer.Option(...)
):
    """Add a character to the pipeline for a project"""
    add_character(project, character, path)


@character_app.command("import")
def character_import(
    character: str = typer.Option(None), project: str = typer.Option(...)
):
    """Import the raw 3D file and transform it."""
    import_character_from_raw(project, character)


@character_app.command("connect")
def character_connect(
    character: str = typer.Option(None),
    mocap: str = typer.Option(None),
    project: str = typer.Option(...),
):
    """Connect a mocap dataset to a character in a project"""
    connect_character_mocap(project, character, mocap)


@character_app.command("rig")
def character_rig(
    character: str = typer.Option(None), project: str = typer.Option(...)
):
    """(Auto)rig a character"""
    rig_character(project, character)
    typer.echo(
        "Currently not enabled. We use auto-rig-pro in blender but recent version change"
        "broke the bpy scripting side of it."
    )
    typer.echo("Open the file in blender, use auto-rig-pro and save.")


@character_app.command("animate")
def character_animate(
    character: str = typer.Option(None),
    animation: str = typer.Option(None),
    project: str = typer.Option(...),
):
    """Add a character to the pipeline for a project"""
    animate_character(project, character, animation)


# publish commands
@app.command()
def publish(
    command: Optional[str] = typer.Argument(None),
    character: str = typer.Option(None),
    animation: str = typer.Option(None),
    project: str = typer.Option(...),
    tag: str = typer.Option(None),
):
    """Add a character to the pipeline for a project"""
    force_all = (command.lower() if command else "") == "all"
    publish_animations(project, character, animation, tag, force_all=force_all)


# navigation utilities (eg info, ls, etc)
@app.command()
def characters(project: str = typer.Option(...)):
    """List all the characters in a project pipeline"""
    obj = UMIGAP.load(project)
    for c in obj.characters.keys():
        typer.echo(c)


@app.command()
def mocaps(project: str = typer.Option(...)):
    """List all the mocap datasets in a project pipeline"""
    obj = UMIGAP.load(project)
    for c in obj.mocaps.keys():
        typer.echo(c)


if __name__ == "__main__":
    app()
