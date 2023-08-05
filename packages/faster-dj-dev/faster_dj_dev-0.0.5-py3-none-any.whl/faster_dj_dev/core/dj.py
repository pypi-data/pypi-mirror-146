import os, subprocess, sys
from termcolor import colored
from colorama import init
from pathlib import Path
#init to enable the color feature in the cmd
init()
# LOCAL IMPORTS
from ..venvs.Pyenv import Venv
from ..data.Pydata import DataUtils
from ..utils.pyUtils import Util

# INITIAL 
venv = Venv()
util = Util()
data = DataUtils()
config = data.get_config_data()

BASE_PATH = Path(__file__).resolve().absolute().parent.parent

class Django:
    def create_new_django_project(self, project_name, app_name=None):
        working_directory = data.get_working_directory_path_from_config_data()
        os.chdir(working_directory)
        venv.install_python_package("django")
        print(f"\nCreating A New Django Project ... {project_name}")
        subprocess.run(f"django-admin startproject {project_name} .", shell=True, stdout=subprocess.PIPE)
        if app_name:
            print(f"\nCreating A New Django App ... {app_name}")
            subprocess.run(f"python manage.py startapp {app_name}", shell=True, stdout=subprocess.PIPE)

    def create_new_django_app(self, app_name):
        installed_apps_list = util.get_installed_apps_list()
        if app_name not in installed_apps_list:
            working_directory = data.get_working_directory_path_from_config_data()
            os.chdir(working_directory)
            print(f"\nCreating A New Django App ... {app_name}")
            subprocess.run(f"python manage.py startapp {app_name}", shell=True, stdout=subprocess.PIPE)
            util.update_installed_apps_list(value=app_name)
        else:
            sys.exit(colored(f"❌ - {app_name} ", "red") +"already exists! Use another app name.")

    def config_django_templates(self):
        working_directory = data.get_working_directory_path_from_config_data()
        os.chdir(working_directory)
        #Creating template and static folders
        if not os.path.isdir("templates"):
            os.mkdir("templates")
            print("[+]\tCreating templates folder ... \n")
        util.update_template_dirs()


    def config_django_static(self):
        working_directory = data.get_working_directory_path_from_config_data()
        os.chdir(working_directory)
        #Creating template and static folders
        if not os.path.isdir("static"):
            os.mkdir("static")
            print("[+]\tCreating static folder ... \n")
        project_name = data.get_project_path_from_config_data()
        project_path = os.path.join(working_directory, project_name)
        settings_file_path = os.path.join(project_path, "settings.py")
        settings = util.get_file_content(settings_file_path)
        if not "STATIC_ROOT" in settings:
            static_settings = util.get_file_content(BASE_PATH / "templates" / "static.py")
            util.add_to_the_bottom_of_the_file(settings_file_path, static_settings)
        

    def config_django_media(self):
        working_directory = data.get_working_directory_path_from_config_data()
        os.chdir(working_directory)
        working_directory = data.get_working_directory_path_from_config_data()
        project_name = data.get_project_path_from_config_data()
        project_path = os.path.join(working_directory, project_name)
        settings_file_path = os.path.join(project_path, "settings.py")
        settings = util.get_file_content(settings_file_path)
        urls_file_path = os.path.join(project_path, "urls.py")
        util.reformat_python_file(urls_file_path)
        if "media" and not os.path.isdir("media"):
            os.mkdir("media")
            venv.install_python_package("Pillow")
            util.add_to_the_top_of_the_file(urls_file_path, "from django.conf import settings\nfrom django.conf.urls.static import static\nfrom django.urls import include\n")
            util.add_to_the_bottom_of_the_file(urls_file_path,"\nurlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)")
            print("[+]\tCreating media folder ... \n")
        if "MEDIA_ROOT" not in settings:
            media_settings = util.get_file_content(BASE_PATH / "templates" / "media.py")
            util.add_to_the_bottom_of_the_file(settings_file_path, media_settings)
        
    def initial_migrate(self):        
        working_directory = data.get_working_directory_path_from_config_data()
        os.chdir(working_directory)
        print(f"\n\n[+]\tMigrating the project ... \n")
        subprocess.run(f'python "manage.py" migrate', shell=True)

    def run_server(self):
        working_directory = data.get_working_directory_path_from_config_data()
        os.chdir(working_directory)
        print(f"\n\n[+]\tRun the server ... \n")
        os.system('pip freeze > "requirements.txt"')
        subprocess.run(f'python "manage.py" runserver', shell=True)

    
    def install_and_config_package(self, package_list):
        working_directory = data.get_working_directory_path_from_config_data()
        os.chdir(working_directory)
        project_name = data.get_project_path_from_config_data()
        project_path = os.path.join(working_directory, project_name)
        urls_file_path = os.path.join(project_path, "urls.py")
        settings_file_path = os.path.join(project_path, "settings.py")
        settings = util.get_file_content(settings_file_path)

        if "djangorestframework" in package_list:
            venv.install_python_package("djangorestframework")
            util.update_installed_apps_list(value="rest_framework")
            util.update_urlpatterns_list(value="path('api-auth/', include('rest_framework.urls'))")

        if "django-cors-headers" in package_list:
            venv.install_python_package("django-cors-headers")
            util.update_installed_apps_list(value="corsheaders")
            util.update_middleware_list(value="corsheaders.middleware.CorsMiddleware", append_after="django.middleware.common.CommonMiddleware")
            util.add_to_the_bottom_of_the_file(settings_file_path, "\n\nDJANGO CORS HEADERS\nCORS_ALLOWED_ORIGINS = [\n\"http://localhost:8080\",\n\"http://127.0.0.1:9000\",\n]")
            util.add_to_the_bottom_of_the_file(settings_file_path, "CORS_ALLOW_CREDENTIALS: True")

        if "django-unicorn" in package_list:
            venv.install_python_package("django-unicorn")
            util.update_installed_apps_list(value="django_unicorn")
            util.update_urlpatterns_list(value="path(\"unicorn/\", include(\"django_unicorn.urls\"))")
            print("\n\n============ DJANGO UNICORN USAGE ===========")
            print(util.get_file_content(os.path.join(BASE_PATH / "templates", "unicorn-base.html")))
            print("Docs URL:\t"+colored("https://www.django-unicorn.com/docs/", "green"))
            print("=======================================\n\n")

        if "tailwind" in package_list:
            venv.install_python_package("django-tailwind") 
            util.update_installed_apps_list(value='tailwind')
            subprocess.run("python manage.py tailwind init", shell=True)
            util.update_installed_apps_list(value='theme')
            if "import platform" not in settings:
                util.add_to_the_top_of_the_file(settings_file_path ,"import platform")
            util.add_to_the_bottom_of_the_file(settings_file_path,"\n\n#DJANGO TAILWIND\n"+util.get_file_content(os.path.join(BASE_PATH / "templates", "tailwind.py")))
            subprocess.run(f"python manage.py tailwind install", shell=True)
            util.update_installed_apps_list(value='django_browser_reload')
            util.update_middleware_list(value="django_browser_reload.middleware.BrowserReloadMiddleware")
            util.update_urlpatterns_list(value="path('__reload__/', include('django_browser_reload.urls'))")
            print("\n\n============ DJANGO TAILWIND USAGE ===========")
            print(util.get_file_content(os.path.join(BASE_PATH / "templates", "tailwind-base.html")))
            print("Docs URL:\t"+colored("https://django-tailwind.readthedocs.io/en/latest/installation.html", "green"))
            print("=======================================\n\n")

        if "django-htmx" in package_list:
            venv.install_python_package("django-htmx")
            util.update_installed_apps_list("django_htmx")
            util.add_to_the_bottom_of_the_file(settings_file_path, "\n\n#DJANGO HTMX\nCRISPY_ALLOWED_TEMPLATE_PACKS = 'tailwind'\nCRISPY_TEMPLATE_PACK = 'tailwind'")
            print("\n\n============ DJANGO HTMX USAGE ===========")
            print(util.get_file_content(os.path.join(BASE_PATH / "templates", "django-htmx-base.html")))
            print("Docs URL:\t"+colored("https://django-htmx.readthedocs.io/en/latest/installation.html", "green"))
            print("=======================================\n\n")

        if "crispy-tailwind" in package_list:
            venv.install_python_package("crispy-tailwind")
            util.update_installed_apps_list("crispy_forms"),
            util.update_installed_apps_list("crispy_tailwind"),
            util.add_to_the_bottom_of_the_file(settings_file_path, '\n\n#TAILWIND CRISPY\nCRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"\nCRISPY_TEMPLATE_PACK = "tailwind"')
            print("\n\n============ DJANGO TAILWIND CRISPY USAGE ===========")
            print(util.get_file_content(os.path.join(BASE_PATH / "templates", "tailwind-crispy.html")))
            print("Docs URL:\t"+colored("https://github.com/django-crispy-forms/crispy-tailwind", "green"))
            print("=======================================\n\n")