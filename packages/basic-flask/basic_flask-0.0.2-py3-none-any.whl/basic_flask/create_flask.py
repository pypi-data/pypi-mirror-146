activate_this='''"""Activate virtualenv for current interpreter:
Use exec(open(this_file).read(), {'__file__': this_file}).
This can be used when you must use an existing Python interpreter, not the virtualenv bin/python.
"""
# source: https://github.com/pypa/virtualenv/blob/main/src/virtualenv/activation/python/activate_this.py

import os
import site
import sys

try:
    abs_file = os.path.abspath(__file__)
except NameError:
    raise AssertionError("You must use exec(open(this_file).read(), {'__file__': this_file}))")

bin_dir = os.path.dirname(abs_file)
base = bin_dir[: -len("__BIN_NAME__") - 1]  # strip away the bin part from the __file__, plus the path separator

# prepend bin to PATH (this file is inside the bin directory)
os.environ["PATH"] = os.pathsep.join([bin_dir] + os.environ.get("PATH", "").split(os.pathsep))
os.environ["VIRTUAL_ENV"] = base  # virtual env is right above bin directory

# add the virtual environments libraries to the host python import mechanism
prev_length = len(sys.path)
for lib in "__LIB_FOLDERS__".split(os.pathsep):
    path = os.path.realpath(os.path.join(bin_dir, lib))
    site.addsitedir(path if "__DECODE_PATH__" else path) # One change was made here path.decode("utf-8") => path
sys.path[:] = sys.path[prev_length:] + sys.path[0:prev_length]

sys.real_prefix = sys.prefix
sys.prefix = base
'''

import subprocess
import secrets
import os
import pathlib

#Path for where the script is runing
path = os.getcwd()

#Path for this file 
this_path = pathlib.Path(__file__).parent.resolve()
def create():
    subprocess.run("python -m venv .venv")
    subprocess.run("mkdir Routes")
    subprocess.run("mkdir Modules")
    subprocess.run("touch main.py .gitignore .env .flaskenv requirements.txt .venv/scripts/activate_this.py")

    with open(f"{path}\\.venv\\scripts\\activate_this.py", "w") as venv_activator:
        venv_activator.write(activate_this)

    # Gitignore write
    with open(f"{path}\\.gitignore", "w") as git:
        git.write(".venv \n__pycache__ ")

    # Basic fleskenv file
    with open(f"{path}\\.flaskenv", "w") as flask_env:
        flask_env.write("FLASK_APP=main.py\nFLASK_ENV=development\nDEBUG=True")

    # Creates env file with random secret key
    with open(f"{path}\\.env", "w") as env:
        env.write(f"SECRET_KEY={secrets.token_hex(48)}\n")

    # Basic flask app
    with open(f"{path}\\main.py", "w") as main:
        main.write('from flask import Flask\nfrom dotenv import load_dotenv\nimport os\n\n\nload_dotenv()\n\napp = Flask(__name__)\napp.config["SECRET_KEY"] = os.getenv("SECRET_KEY")')

    activator = f"{path}\\.venv\\scripts\\activate_this.py"
    with open(activator) as f:
        exec(f.read(), {'__file__': activator})

    subprocess.run("pip install flask python-dotenv")

    with open(f"{path}\\requirements.txt", "w") as requirements:
        subprocess.run("pip3 freeze > requirements.txt", stdout=requirements)







