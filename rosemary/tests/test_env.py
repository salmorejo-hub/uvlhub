import os
from unittest import mock

from click.testing import CliRunner

from rosemary.commands.env import env


def test_env_command_with_mocked_env_file(tmp_path):
    runner = CliRunner()

    env_file = tmp_path / ".env"
    env_content = "VAR1=value1\nVAR2=value2\n"
    env_file.write_text(env_content)

    with mock.patch.dict(os.environ, {"WORKING_DIR": str(tmp_path)}):
        result = runner.invoke(env)

    assert result.exit_code == 0

    assert "VAR1=value1" in result.output
    assert "VAR2=value2" in result.output


def test_env_command_with_missing_env_file(tmp_path):
    runner = CliRunner()

    with mock.patch.dict(os.environ, {"WORKING_DIR": str(tmp_path)}):
        result = runner.invoke(env)

    assert result.exit_code == 0
    assert result.output.strip() == ""
