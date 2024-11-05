import os
import subprocess

import click
from dotenv import load_dotenv


@click.command('db:table', help="Select the first 5 rows from the table given as a paremeter.")
@click.argument('table')
def db_table(table):
    load_dotenv()
    
    mariadb_hostname = os.getenv('MARIADB_HOSTNAME')
    mariadb_user = os.getenv('MARIADB_USER')
    mariadb_password = os.getenv('MARIADB_PASSWORD')
    mariadb_database = os.getenv('MARIADB_DATABASE')
    
    sql_command = f"SELECT * FROM {table} LIMIT 5;"
    maria_db_command = f'mysql -h{mariadb_hostname} -u{mariadb_user} -p{mariadb_password} {mariadb_database} -e "{sql_command}"'
        
    # Execute the command
    try:
        subprocess.run(maria_db_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        click.echo(click.style(f"Error opening MariaDB console: {e}", fg='red'))

    