import subprocess
import click
import shutil


@click.command('run:app', help="Run the app server, Discord bot, and FakeNodo in separate terminal windows")
def run_app():

    TERMINAL_OPTIONS = ["gnome-terminal", "x-terminal-emulator", "konsole"]

    terminal = None
    flask_run_command = "flask run --host=0.0.0.0 --reload --debug"
    fakenodo_run_command = "python fakenodo/run.py"
    discord_bot_run_command = "python discordbot/__init__.py"

    # Get the first terminal  that is available
    terminal = next((term for term in TERMINAL_OPTIONS if shutil.which(term) is not None), None)

    if terminal is None:
        click.echo(click.style(f"No terminal found. Please install one of the following: {TERMINAL_OPTIONS}",
                               fg='red'))
        return

    try:
        subprocess.Popen([terminal, "--", "bash", "-c", f"{flask_run_command}; exec bash"])
        subprocess.Popen([terminal, "--", "bash", "-c", f"{fakenodo_run_command}; exec bash"])
        subprocess.Popen([terminal, "--", "bash", "-c", f"{discord_bot_run_command}; exec bash"])
    except subprocess.CalledProcessError as e:
        click.echo(click.style(f"Error: {e}", fg='red'))
