import os
import toml


def sync_version():
    pyproject_path = 'pyproject.toml'
    with open(pyproject_path, 'r') as f:
        pyproject = toml.load(f)
        version = pyproject['project']['version']

    version_file_path = os.path.join('cmoat', 'version.py')
    with open(version_file_path, 'w') as f:
        f.write(f'__version__ = "{version}" # Setup by CI/CD\n')
        print(
            f"Sync version to {version_file_path} with {version} successfully!")


if __name__ == "__main__":
    sync_version()
