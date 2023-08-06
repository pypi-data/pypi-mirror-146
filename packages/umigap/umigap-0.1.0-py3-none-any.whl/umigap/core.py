"""
UMIGAP -- Up Multimedia Indie Game Animation Pipeline

USE AT OWN RISK

GPL3
"""

from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Optional


from dataclasses_json import dataclass_json
from ruamel.yaml import YAML, round_trip_dump


def load_project(slug: str):
    """ Load from yaml """
    project_yaml_file = Path(Path(slug) / Path(slug)).with_suffix(".yaml")
    with open(project_yaml_file) as file:
        yaml = YAML()
        project = yaml.load(file)
    return UMIGAP.from_dict(project)


def save_project(slug: str, data: dict):
    """ Save to yaml """
    project_yaml_file = Path(Path(slug) / Path(slug)).with_suffix(".yaml")
    with open(project_yaml_file, "w") as f:
        f.write(
            round_trip_dump(data, indent=4, block_seq_indent=2)
        )
    return True


@dataclass_json
@dataclass
class Tool:
    """ A 3rd party tool used by the pipeline, eg for mocap or rigging """
    version: Optional[str] = ""
    stages: List[str] = field(default_factory=list)  # list of stages this tool might be used for


@dataclass_json
@dataclass
class Vector3:
    x: float = 0
    y: float = 0
    z: float = 0


@dataclass_json
@dataclass
class RawDetail:
    """ Link to a row art asset """
    input: str = ""  # input file
    output: str = ""  # transformed output file
    scale: float = 1.0
    rotate: Vector3 = Vector3(0, 0, 0)   # degrees
    translate: Vector3 = Vector3(0, 0, 0)  # in metres
    decimate_layers: Optional[Dict[str, float]] = field(default_factory=dict)  # dict of layers to decimate and values
    drop_pivot: bool = False  # drop the pivot to the floor
    volume_pivot_layers: Optional[List[str]] = field(default_factory=list)  # layers to move pivot to volume centre


@dataclass_json
@dataclass
class RigDetail:
    """ Hints for autorigging """
    layer: str = ""  # which layer is the riggable component of the art asset
    input: Optional[str] = ""  # if empty use raw detail output
    output: Optional[str] = ""  # if empty, place in rigged/
    neck: Optional[Vector3] = None
    chin: Optional[Vector3] = None
    shoulder_left: Optional[Vector3] = None
    shoulder_right: Optional[Vector3] = None
    wrist_left: Optional[Vector3] = None
    wrist_right: Optional[Vector3] = None
    spine_root: Optional[Vector3] = None
    ankle_left: Optional[Vector3] = None
    ankle_right: Optional[Vector3] = None


@dataclass_json
@dataclass
class AnimationDetail:
    """ Link a character to a mocap dataset """
    description: str = ""
    mocap: str = ""   # Stub from UMIGAP.mocaps
    output: Optional[str] = ""
    looping: bool = True
    autoplay: bool = True
    disabled_layers: Optional[List[str]] = field(default_factory=list)
    tags: Optional[List[str]] = field(default_factory=list)   # allow groups eg "dancing"


@dataclass_json
@dataclass
class Character:
    """ A character in our pipeline"""
    name: str = "Untitled Character"
    raw: Optional[RawDetail] = None
    rig: Optional[RigDetail] = None
    animations: Optional[Dict[str, AnimationDetail]] = field(default_factory=dict)


@dataclass_json
@dataclass
class Mocap:
    """ A mocap sequence in our pipeline"""
    name: str = "Untitled Mocap"
    tool: str = "unknown-mocap-tool"
    input: str = ""  # input file to tool
    output: str = ""  # name of bvh export from tool
    start: int = 0  # start frame of input
    end: int = 0  # end from of unput
    primary: str = ""  # primary character this applies to, for test hinting


@dataclass_json
@dataclass
class UMIGAP:
    """
    Class for interacting with a umigap yaml file.
    """
    name: str = "Untitled Project"
    target: str = "godot3"
    slug: str = "untitled"
    version: Optional[str] = "1.0.0"
    tools: Optional[Dict[str, Tool]] = field(default_factory=dict)
    mocaps: Optional[Dict[str, Mocap]] = field(default_factory=dict)
    characters: Optional[Dict[str, Character]] = field(default_factory=dict)

    stages: Optional[List[str]] = field(default_factory=list)  # stages available in umigap

    @classmethod
    def load(cls, slug):
        """ Load from yaml into class """
        return load_project(slug)

    def save(self):
        """ Save obj to yaml """
        return save_project(self.slug, asdict(self, dict_factory=lambda x: {k: v for (k, v) in x if v is not None}))

    def add_character(self, slug):
        """ Add a character to the obj """
        self.characters[slug] = Character()

    def add_mocap(self, slug):
        self.mocaps[slug] = Mocap()

    def add_tool(self, slug, stages=None):
        if not stages:
            stages = []
        self.tools[slug] = Tool(stages=stages)
