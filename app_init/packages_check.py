import sys
import importlib
from typing import Callable, Optional

# The package list that need to be installed for this APP
dependence_packages: list[str] = ['numpy', 'pandas', 'matplotlib', 'seaborn', 'cptac', 'scipy']

def get_uninstalled_packages(dependence_packages: list[str] = dependence_packages) -> list[str]:
    """
    Get uninstalled package from dependence_packages, the default dependence_packages is the global variable dependence_packages
    """
    uninstalled_package: list[str] = []
    for package in dependence_packages:
        try:
            importlib.import_module(package)
        except ModuleNotFoundError:
            uninstalled_package.append(package)
    return uninstalled_package


def install_packages(packages: list[str],
                    pkg_install_start_cb: Optional[Callable[[str], None]] = None,
                    pkg_install_finished_cb: Optional[Callable[[str], None]] = None,
                    pkg_install_unfinished_cb: Optional[Callable[[str], None]] = None) -> None:
    """
    Install packages from input pkg name list
    """
    import subprocess

    for package in packages:
        if pkg_install_start_cb is not None:
            pkg_install_start_cb(package)
        
        is_installed = subprocess.check_call([sys.executable, "-m", "pip", "install", package])

        # import time
        # time.sleep(2)

        is_installed = True
        if(is_installed):
            if pkg_install_finished_cb is not None:
                pkg_install_finished_cb(package)
        elif pkg_install_unfinished_cb is not None:
            pkg_install_unfinished_cb(package)

def test() -> None:
    uninstalled_packages = get_uninstalled_packages(['numpy'])
    if len(uninstalled_packages) > 0:
        install_packages(uninstalled_packages
                         , lambda pkg: print(f"Start to install {pkg}")
                         , lambda pkg: print(f"Finished install {pkg}"
                         , lambda pkg: print(f"Failed to install {pkg}")))

if __name__ == "__main__":
    test()