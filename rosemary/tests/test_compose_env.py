import os
import tempfile

from click.testing import CliRunner
from dotenv import dotenv_values

from rosemary.commands.compose_env import compose_env


def test_compose_env_with_no_conflicts():
    with tempfile.TemporaryDirectory() as temp_dir:
        os.environ['WORKING_DIR'] = temp_dir

        root_env_path = os.path.join(temp_dir, '.env')
        with open(root_env_path, 'w') as root_file:
            root_file.write("KEY1=value1\nKEY2=value2\n")

        module_dir = os.path.join(temp_dir, 'app/modules/module')
        os.makedirs(module_dir)
        module_env_path = os.path.join(module_dir, '.env')
        with open(module_env_path, 'w') as module1_file:
            module1_file.write("KEY3=value3\nKEY4=value4\n")

        runner = CliRunner()
        result = runner.invoke(compose_env)

        assert result.exit_code == 0
        assert "Successfully merged .env files without conflicts." in result.output

        merged_env_vars = dotenv_values(root_env_path)
        assert merged_env_vars["KEY1"] == "value1"
        assert merged_env_vars["KEY2"] == "value2"
        assert merged_env_vars["KEY3"] == "value3"
        assert merged_env_vars["KEY4"] == "value4"


def test_compose_env_with_conflicts():
    with tempfile.TemporaryDirectory() as temp_dir:
        os.environ['WORKING_DIR'] = temp_dir

        root_env_path = os.path.join(temp_dir, '.env')
        with open(root_env_path, 'w') as root_file:
            root_file.write("KEY1=value1\nKEY2=value2\n")

        module1_dir = os.path.join(temp_dir, 'app/modules/module1')
        os.makedirs(module1_dir)
        module1_env_path = os.path.join(module1_dir, '.env')
        with open(module1_env_path, 'w') as module1_file:
            module1_file.write("KEY2=conflicting_value\nKEY3=value3\n")

        module2_dir = os.path.join(temp_dir, 'app/modules/module2')
        os.makedirs(module2_dir)
        module2_env_path = os.path.join(module2_dir, '.env')
        with open(module2_env_path, 'w') as module2_file:
            module2_file.write("KEY4=value4\n")

        runner = CliRunner()
        result = runner.invoke(compose_env)

        assert result.exit_code == 0
        assert "Conflict found for variable 'KEY2'" in result.output
        assert "Successfully merged .env files without conflicts." in result.output

        merged_env_vars = dotenv_values(root_env_path)
        assert merged_env_vars["KEY1"] == "value1"
        assert merged_env_vars["KEY2"] == "value2"
        assert merged_env_vars["KEY3"] == "value3"
        assert merged_env_vars["KEY4"] == "value4"
