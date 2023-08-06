"""
UMIGAP -- Up Multimedia Indie Game Animation Pipeline

USE AT OWN RISK

GPL3
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

from dataclasses_json import dataclass_json
from ruamel.yaml import YAML, round_trip_dump

try:
    from importlib import metadata
except ImportError:  # for Python<3.8
    import importlib_metadata as metadata

__version__ = metadata.version("umigap")


@dataclass_json
@dataclass
class Tool:
    """A 3rd party tool used by the pipeline, eg for mocap or rigging"""

    name: Optional[str] = None
    uri: Optional[str] = None
    version: Optional[str] = None
    formats: Optional[List[str]] = None  # eg request tool to deliver .GLB, .FBX, .blend
    stage: Optional[str] = None  # stage this is used for


@dataclass_json
@dataclass
class Vector3:
    """Basic 3D Vector"""

    x: float = 0
    y: float = 0
    z: float = 0


@dataclass_json
@dataclass
class RawDetail:
    """Link to a row art asset"""

    tool: Optional[str] = None  # tool used to generate the transformed output file
    scale: Optional[float] = None  # float
    rotate: Optional[Vector3] = None  # degrees
    translate: Optional[Vector3] = None  # in metres
    decimate_layers: Optional[Dict[str, float]] = field(
        default_factory=dict
    )  # dict of layers to decimate and values
    drop_pivot: bool = False  # drop the pivot to the floor
    volume_pivot_layers: Optional[List[str]] = field(
        default_factory=list
    )  # layers to move pivot to volume centre


@dataclass_json
@dataclass
class RigDetail:
    """Hints for autorigging"""

    layer: str = ""  # which layer is the riggable component of the art asset
    tool: Optional[str] = None  # tool used to generate the rigged output file
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
class AnimationConnection:
    """Link a character to a mocap dataset"""

    description: str = ""
    mocap: str = ""  # Stub from UMIGAP.mocaps, character contains the other link (ie it links to the connection)
    tool: Optional[str] = None  # tool used to generate the rigged output file
    looping: Optional[bool] = None
    autoplay: Optional[bool] = None
    disabled_layers: Optional[List[str]] = field(default_factory=list)
    draft: Optional[bool] = None
    tags: Optional[List[str]] = field(default_factory=list)  # allow groups eg "dancing"


@dataclass_json
@dataclass
class Mocap:
    """A mocap sequence in our pipeline"""

    name: str = "Untitled Mocap"
    input: Optional[str] = None  # input file to tool
    # output: Optional[str] = None  # name of bvh export from tool
    description: Optional[str] = None
    tool: Optional[str] = None  # tool used to generate the output BVH file
    start: Optional[int] = None  # start frame of input
    end: Optional[int] = None  # end from of unput
    primary: Optional[str] = None  # primary character this applies to, for test hinting


@dataclass_json
@dataclass
class Character:
    """A character in our pipeline"""

    name: str = "Untitled Character"
    input: str = ""  # input file  (ie the initial raw art asset)
    raw: Optional[str] = None  # from list of raw
    rig: Optional[str] = None  # from list of rigs
    animations: Optional[List[str]] = None  # list of AnimationConnection keys
    tags: Optional[List[str]] = None  # allow groups eg "dancing"


@dataclass_json
@dataclass
class UMIGAP:
    """
    Class for interacting with a umigap yaml file.
    """

    name: str = "Untitled Project"
    target: str = "godot3"
    slug: str = "untitled"
    version: Optional[str] = __version__
    tools: Optional[Dict[str, Tool]] = field(default_factory=dict)
    mocaps: Optional[Dict[str, Mocap]] = field(default_factory=dict)
    characters: Optional[Dict[str, Character]] = field(default_factory=dict)
    animations: Optional[Dict[str, AnimationConnection]] = field(default_factory=dict)
    rigs: Optional[Dict[str, RigDetail]] = field(default_factory=dict)
    raw: Optional[Dict[str, RawDetail]] = field(default_factory=dict)

    stages: Optional[List[str]] = field(
        default_factory=list
    )  # stages available in umigap

    def get_save_path(self):
        return Path(Path(self.slug) / Path(self.slug)).with_suffix(".yaml")

    @classmethod
    def load(cls, slug) -> UMIGAP:
        """Load from yaml into class"""
        return load_project(slug)

    def save(self):
        """Save obj to yaml"""
        return save_project(
            self.slug,
            asdict(
                self, dict_factory=lambda x: {k: v for (k, v) in x if v is not None}
            ),
        )

    def add_character(self, slug, obj=None):
        """Add a character to the obj"""
        if not obj:
            obj = Character()
        self.characters[slug] = obj

    def add_mocap(self, slug, obj=None):
        if not obj:
            obj = Mocap()
        self.mocaps[slug] = obj

    def add_tool(self, slug, obj=None):
        if not obj:
            obj = Tool()
        self.tools[slug] = obj

    def add_raw(self, slug, obj=None, for_character_slug=None):
        if not obj:
            obj = RawDetail()

        character = self.find_character(for_character_slug)
        if character:
            character.raw = slug
            output = Path("ready_to_rig") / Path(for_character_slug)
            output.mkdir(parents=True, exist_ok=True)

        self.raw[slug] = obj

    def add_rig(self, slug, obj=None, for_character_slug=None):
        if not obj:
            obj = RigDetail()

        character = self.find_character(for_character_slug)
        if character:
            character.rig = slug

        self.rigs[slug] = obj

    def add_animation(self, slug, obj=None, for_character_slug=None):
        if not obj:
            obj = AnimationConnection()

        character = self.find_character(for_character_slug)
        if not character.animations:
            character.animations = []
        if character and slug not in character.animations:
            character.animations.append(slug)

        self.animations[slug] = obj

    def find_character(self, character_slug: str):
        return self.characters.get(character_slug, None)

    def find_tool_for_stage(self, stage: str):
        """Find the first tool that works on this stage"""
        for key, tool in self.tools.items():
            if stage == tool.stage:
                return key
        return None


def load_project(slug: str) -> UMIGAP:
    """Load from yaml"""
    project_yaml_file = Path(Path(slug) / Path(slug)).with_suffix(".yaml")
    with open(project_yaml_file) as file:
        yaml = YAML()
        project = yaml.load(file)
    return UMIGAP.from_dict(project)


def save_project(slug: str, data: dict):
    """Save to yaml"""
    project_yaml_file = Path(Path(slug) / Path(slug)).with_suffix(".yaml")
    with open(project_yaml_file, "w") as f:
        f.write(round_trip_dump(data, indent=2, block_seq_indent=2))
    return True
