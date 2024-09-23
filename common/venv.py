#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Reiner New
email: nbxlc@hotmail.com
"""

import subprocess
import venv
import virtualenv



def create_venv(env_name):
    if not env_name:
        print("Please enter a valid name.")
        return (False, "Please enter a valid name.")

    # Create virtual environment
    # result = subprocess.run(['python', '-m', 'venv ', env_name], capture_output=True, text=True)
    # if result.returncode == 0:
    #     print(f"Virtual environment '{env_name}' created successfully.")
    #     return (True, f"Virtual environment '{env_name}' created successfully.")
    # else:
    #     print(f"Error: {result.stderr}")
    #     return (False, f"Error: {result.stderr}")

    # virtualenv.cli_run([env_name, "--pip", "23"])
    virtualenv.cli_run([env_name, '--python=python3.9.10'])

    # result = subprocess.run(['python', '-m', 'virtualenv', env_name, '--pip', 'latest'], capture_output=True, text=True)
    # if result.returncode == 0:
    #     print(f"Virtual environment '{env_name}' created successfully.")
    # else:
    #     print(f"Error: {result.stderr}")


class VenvManager:
    def create_venv(self, env_name):
        virtualenv.cli_run([env_name, "--pip", "23"])

    def activate_venv(self, path):
        if sys.platform == "win32":
            activate_script = f"{path}\\Scripts\\activate.bat"
        else:
            activate_script = f"source {path}/bin/activate"

        subprocess.run(activate_script, shell=True)

    def install_package(self, package_name):
        subprocess.run([f"{self.venv_path}/bin/pip", "install", package_name])



if __name__ == "__main__":
    create_venv("myVE")
    # cli_run(["myVE"])
    # create_environment("myVE")
    # print("done")
    # asyncio.run(install_virtualenv("myVE"))