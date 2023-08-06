from .core import UMIGAP, Tool


class TestCore:
    def test_find_tool_for_stage(self):
        obj = UMIGAP("test")
        obj.add_tool("my_tool", Tool(stage="rig"))
        assert obj.find_tool_for_stage("rig") is not None
