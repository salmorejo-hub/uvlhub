import os
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from rosemary.commands.coverage import coverage


@pytest.fixture
def mock_working_dir(tmp_path):
    working_dir = tmp_path / "app/modules"
    working_dir.mkdir(parents=True, exist_ok=True)
    os.environ["WORKING_DIR"] = str(tmp_path)
    return working_dir


@patch("subprocess.run")
def test_coverage_with_no_module(mock_run, mock_working_dir):
    runner = CliRunner()
    result = runner.invoke(coverage)
    assert result.exit_code == 0
    assert "Running coverage for all modules..." in result.output
    mock_run.assert_called_once_with(
        ['pytest', '--ignore-glob=*selenium*', '--cov=' + str(mock_working_dir), str(mock_working_dir)],
        check=True,
    )


@patch("subprocess.run")
def test_coverage_with_valid_module(mock_subprocess, mock_working_dir):
    valid_module_name = "module"
    os.mkdir(mock_working_dir / valid_module_name)

    runner = CliRunner()
    result = runner.invoke(coverage, [valid_module_name])

    assert result.exit_code == 0
    assert f"Running coverage for the '{valid_module_name}' module..." in result.output
    mock_subprocess.assert_called_once_with(
        ['pytest', '--ignore-glob=*selenium*', '--cov=' + str(mock_working_dir / valid_module_name),
         str(mock_working_dir / valid_module_name)], check=True,
    )


def test_coverage_with_invalid_module():
    invalid_module_name = "invalid_module"

    runner = CliRunner()
    result = runner.invoke(coverage, [invalid_module_name])

    assert result.exit_code == 0
    assert f"Module '{invalid_module_name}' does not exist." in result.output


@patch("subprocess.run")
def test_coverage_with_module_and_html(mock_subprocess, mock_working_dir):
    valid_module_name = "valid_module"
    os.mkdir(mock_working_dir / valid_module_name)

    runner = CliRunner()
    result = runner.invoke(coverage, [valid_module_name, "--html"])

    assert result.exit_code == 0
    assert f"Running coverage for the '{valid_module_name}' module..." in result.output
    mock_subprocess.assert_called_once_with(
        [
            'pytest', '--ignore-glob=*selenium*', '--cov=' + str(mock_working_dir / valid_module_name),
            str(mock_working_dir / valid_module_name), '--cov-report', 'html'
        ],
        check=True,
    )
