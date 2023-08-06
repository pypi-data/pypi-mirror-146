import os
import tempfile

from ruamel.yaml import YAML, round_trip_dump

from .utils import create_project


class TestUtils:
    def test_create_project(self):
        with tempfile.TemporaryDirectory() as tmp_path:
            os.chdir(tmp_path)
            obj = create_project("glamnoir", "Glam Noir", "godot3")

            with open(obj.get_save_path()) as f:
                yaml = YAML()
                project = yaml.load(f)

            assert project["name"] == "Glam Noir"
