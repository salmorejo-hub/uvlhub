from click.testing import CliRunner

from rosemary.commands.module_list import module_list


def test_module_list():
    runner = CliRunner()
    result = runner.invoke(module_list)

    assert result.exit_code == 0
    assert "Loaded Modules" in result.output
    assert "Ignored Modules" in result.output
