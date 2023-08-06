"""
 pytest
"""
import os
import tempfile

from .cli import (
    character_add,
    character_animate,
    character_connect,
    character_import,
    character_rig,
    init,
    mocap_add,
    mocap_import,
    publish,
)
from .core import UMIGAP


class TestScenarios:
    def test_start_to_end(self):
        """
        poetry run umigap init test
        poetry run umigap character add leo.glb --project test --character leo
        poetry run umigap character import --project test --character leo
        poetry run umigap character rig --project test --character leo
        poetry run umigap mocap add rehearse.raw --project test --mocap rehearse
        poetry run umigap mocap import --project test --mocap rehearse
        poetry run umigap character connect --project test --character leo --mocap rehearse
        poetry run umigap character animate --project test --animation leo_rehearse
        poetry run umigap publish all  --project test
        """
        with tempfile.TemporaryDirectory() as tmp_path:
            os.chdir(tmp_path)
            init("glam_noir")
            character_add("leo_raw.glb", "Leo", "glam_noir"),
            character_import("Leo", "glam_noir")
            character_rig("Leo", "glam_noir")
            mocap_add("dance_raw.raw", "dance", "glam_noir")
            mocap_import("dance", "glam_noir")
            character_connect("Leo", "dance", "glam_noir")
            character_animate("Leo", "leo_dance", "glam_noir")
            publish("all", project="glam_noir")
            obj = UMIGAP.load("glam_noir")

            assert len(obj.rigs) == 1
            assert len(obj.rigs) == 1
            assert len(obj.mocaps) == 1
            assert len(obj.characters) == 1
            assert len(obj.tools) == 4
            assert len(obj.stages) == 5
