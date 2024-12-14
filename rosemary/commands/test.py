import click
import subprocess
import os
import signal


@click.command('test', help="Runs pytest on the blueprints directory or a specific module.")
@click.argument('module_name', required=False)
@click.option('-k', 'keyword', help="Only run tests that match the given substring expression.")
def test(module_name, keyword):
    base_path = os.path.join(os.getenv('WORKING_DIR', ''), 'app/modules')
    test_path = base_path

    if module_name:
        test_path = os.path.join(base_path, module_name)
        if not os.path.exists(test_path):
            click.echo(click.style(f"Module '{module_name}' does not exist.", fg='red'))
            return
        click.echo(f"Running tests for the '{module_name}' module...")
    else:
        click.echo("Running tests for all modules...")

    pytest_cmd = ['pytest', '-v', '--ignore-glob=*selenium*', test_path]

    if keyword:
        pytest_cmd.extend(['-k', keyword])

    try:
        subprocess.run(pytest_cmd, check=True)
    except subprocess.CalledProcessError as e:
        click.echo(click.style(f"Error running tests: {e}", fg='red'))

    if not module_name:
        _test_discord_bot()
        _test_rosemary()
        _test_fakenodo()


def _test_discord_bot():
    click.echo("Running tests for the discord bot...")
    click.echo("In order to run the discordbot tests, the application must be running.")
    click.echo("Do you want to run the application now? [y/N]")

    if input().lower() != 'y':
        return

    discordbot_test_path = os.path.join(os.getenv('WORKING_DIR', ''), 'discordbot')
    discordbot_test_cmd = ['pytest', '-v', '--ignore-glob=*selenium*', discordbot_test_path]
    run_app_cmd = ["flask", "run", "--host=0.0.0.0", "--reload", "--debug"]

    flask_process = None

    try:
        flask_process = subprocess.Popen(run_app_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                         preexec_fn=os.setsid)
        click.echo("Waiting for Flask application to start...")
        subprocess.run(discordbot_test_cmd, check=True)
    except subprocess.CalledProcessError as e:
        click.echo(click.style(f"Error running discord tests: {e}.", fg='red'))
    finally:
        if flask_process:
            click.echo("Stopping the Flask application...")
            os.killpg(os.getpgid(flask_process.pid), signal.SIGTERM)


def _test_rosemary():
    click.echo("Running tests for the rosemary CLI...")
    rosemary_test_path = os.path.join(os.getenv('WORKING_DIR', ''), 'rosemary')
    rosemary_test_cmd = ['pytest', '-v', '--ignore-glob=*selenium*', rosemary_test_path]
    try:
        subprocess.run(rosemary_test_cmd, check=True)
    except subprocess.CalledProcessError as e:
        click.echo(click.style(f"Error running rosemary tests: {e}.", fg='red'))


def _test_fakenodo():
    click.echo("Running tests for fakenodo...")
    fakenodo_test_path = os.path.join(os.getenv('WORKING_DIR', ''), 'fakenodo')
    fakenodo_test_cmd = ['pytest', '-v', '--ignore-glob=*selenium*', fakenodo_test_path]
    try:
        subprocess.run(fakenodo_test_cmd, check=True)
    except subprocess.CalledProcessError as e:
        click.echo(click.style(f"Error running rosemary tests: {e}.", fg='red'))


if __name__ == '__main__':
    test()
