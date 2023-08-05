import subprocess
import secrets
import os
import pathlib
import shutil

#Path for where the script is runing
path = os.getcwd()

#Path for this file 
this_path = pathlib.Path(__file__).parent.resolve()

def create():

    subprocess.run("python -m venv .venv")
    subprocess.run("mkdir Routes")
    subprocess.run("mkdir Modules")
    subprocess.run("touch .env requirements.txt .gitignore .flaskenv")

    shutil.copy(f"{this_path}\\creation_files\\activate_this.py", f"{path}\\.venv\\scripts\\activate_this.py")
    shutil.copy(f"{this_path}\\creation_files\\main.py", f"{path}\\main.py")

    # Creates env file with random secret key 
    with open(f"{path}\\.env", "w") as env:
        env.write(f'SECRET_KEY="{secrets.token_hex(48)}"\n')

    # Create .gitignore with some data
    with open(f"{path}\\.gitignore", "w") as env:
        env.write(".venv \n__pycache__\n")
    
    # Create .flaskenv with some data
    with open(f"{path}\\.flaskenv", "w") as env:
        env.write("FLASK_APP=main.py\nFLASK_ENV=development\nDEBUG=True\n")

    # active the new venv
    activator = f"{path}\\.venv\\scripts\\activate_this.py"
    with open(activator) as f:
        exec(f.read(), {'__file__': activator})

    # installing the modules in the venv
    subprocess.run("pip install flask python-dotenv")

    # updating requirements.txt
    with open(f"{path}\\requirements.txt", "w") as requirements:
        subprocess.run("pip3 freeze > requirements.txt", stdout=requirements)
