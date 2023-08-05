from pathlib import Path
import time, os, sys
while True:
    try:
        from termcolor import colored
        from colorama import init
        import click
        #init to enable the color feature in the cmd
        init()
    except (ImportError, ModuleNotFoundError):
        os.system("python -m pip install click==8.1.0 colorama==0.4.4 termcolor==1.1.0 black==22.3.0")
        time.sleep(1)
    else:
        break

# LOCAL IMPORTS
from .core.dj import Django
from .venvs.Pyenv import Venv
from .data.Pydata import DataUtils
from .utils.pyUtils import Util

# INITIAL
django = Django()
Pyvenv = Venv()
util = Util()
data = DataUtils()
config = data.get_config_data()

@click.command()
@click.option("--create-project", "-cp", is_flag=True, help="Install a new Django project.")
@click.option("--config-templates", "-ct", is_flag=True, help="Create templates folder and update settings.")
@click.option("--config-static", "-cs", is_flag=True, help="Create static folder and update settings.")
@click.option("--config-media", "-cm", is_flag=True, help="Create media folder and update settings.")
@click.option("--initial-migrate", "-im", is_flag=True, help="Run the migration after creating a new Django project.")
@click.option("--run-server", "-rs", is_flag=True, help="Run the local server.")
@click.option("--install", "-i",multiple=True, type=click.Choice([
    "djangorestframework", "django-cors-headers", "crispy-tailwind", "django-unicorn", "tailwind", "django-htmx"
    ],case_sensitive=False ), help="Install Django package.")
@click.option("--app", "-a", type=str, help="specify the application name.")
def main(
        create_project, app, config_templates, config_static, config_media, initial_migrate, run_server, install
    ):

    # Print system info
    os_version, pip_version, python_version = util.get_system_data()
    print("Operating system: "+colored(os_version, "blue"))
    print("Python version: "+colored(python_version, "blue"))
    print("Pip version: "+colored(pip_version, "blue"))

    
    if not Pyvenv.is_venv_activated():
        print("\nYour virtual environment is not activated.\n"+colored("Options:", "blue")+"\n")
        print("1-\tActivate it.\n2-\tUse the --venv flag.")
    
    else:
        if create_project:
            project = data.get_project_path_from_config_data()
            django.create_new_django_project(project)
                
        if app:
            django.create_new_django_app(app)
            config["app_names"].append(app)
            data.update_data_config(config_dict=config)

        if config_templates:
            django.config_django_templates()

        if config_static:
            django.config_django_static()

        if config_media:
            django.config_django_media()

        if initial_migrate:
            django.initial_migrate()

        if run_server:    
            django.run_server()

        if install:
            django.install_and_config_package(install)

if __name__ == "__main__":
    main()