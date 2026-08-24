from cad_bim.capabilities import describe_capabilities
from cad_bim.cli import main


def test_list_command_prints_core_capabilities() -> None:
    text = describe_capabilities()
    assert "IFC4" in text
    assert "STEP AP214" in text
    assert "我做不到" in text


def test_cli_list(capsys) -> None:
    assert main(["list"]) == 0
    assert "直接改" in capsys.readouterr().out
