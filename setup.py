import subprocess
import sys

def install_missing_dependencies(requirements_file="requirements.txt"):
    try:
        with open(requirements_file, "r") as f:
            requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        print(f"Error: Requirements file '{requirements_file}' not found.")
        return

    installed_packages = {pkg.split("==")[0].lower() for pkg in subprocess.check_output([sys.executable, '-m', 'pip', 'freeze']).decode().splitlines()}

    missing_dependencies = []
    for req in requirements:
        package_name = req.split("==")[0].lower()
        if package_name not in installed_packages:
            missing_dependencies.append(req)

    if missing_dependencies:
        print("Installing missing dependencies:")
        for dep in missing_dependencies:
            print(f"- {dep}")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing_dependencies])
            print("All missing dependencies installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error installing dependencies: {e}")
    else:
        print("All dependencies in requirements file are already installed.")

if __name__ == "__main__":
    install_missing_dependencies()