import os
import shutil
import tempfile

from click.testing import CliRunner

from core.configuration.configuration import uploads_folder_name
from rosemary.commands.clear_uploads import clear_uploads


def test_clear_uploads_existing():
    with tempfile.TemporaryDirectory() as temp_dir:
        os.environ['WORKING_DIR'] = temp_dir

        uploads_dir_path = os.path.join(temp_dir, uploads_folder_name())
        os.mkdir(uploads_dir_path)

        runner = CliRunner()
        result = runner.invoke(clear_uploads)

        assert result.exit_code == 0
        assert not os.path.exists(uploads_dir_path)
        assert "The 'uploads' directory has been successfully cleared." in result.output


def test_clear_log_unexisting():
    with tempfile.TemporaryDirectory() as temp_dir:
        os.environ['WORKING_DIR'] = temp_dir

        uploads_dir_path = os.path.join(temp_dir, uploads_folder_name())
        if os.path.exists(uploads_dir_path) and os.path.isdir(uploads_dir_path):
            shutil.rmtree(uploads_dir_path)

        runner = CliRunner()
        result = runner.invoke(clear_uploads)

        assert result.exit_code == 0
        assert "The 'uploads' directory does not exist." in result.output
