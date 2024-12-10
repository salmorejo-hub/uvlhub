import os
import tempfile

from click.testing import CliRunner

from rosemary.commands.clear_log import clear_log


def test_clear_log_existing():
    with tempfile.TemporaryDirectory() as temp_dir:
        os.environ['WORKING_DIR'] = temp_dir

        log_file_path = os.path.join(temp_dir, 'app.log')
        with open(log_file_path, 'w') as f:
            f.write("Test log content")

        runner = CliRunner()
        result = runner.invoke(clear_log)

        assert result.exit_code == 0
        assert not os.path.exists(log_file_path)
        assert "The 'app.log' file has been successfully cleared." in result.output


def test_clear_log_unexisting():
    with tempfile.TemporaryDirectory() as temp_dir:
        os.environ['WORKING_DIR'] = temp_dir

        log_file_path = os.path.join(temp_dir, 'app.log')
        if os.path.exists(log_file_path):
            os.remove(log_file_path)

        runner = CliRunner()
        result = runner.invoke(clear_log)

        assert result.exit_code == 0
        assert "The 'app.log' file does not exist." in result.output
