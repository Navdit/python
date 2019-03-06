import time
import importlib
from pip._internal import main as pipmain
import data.global_variables as global_var


# FUNCTION - Installs the given Module in Python
def install(package):
    pipmain(['install', package])


# Reads Requirements from Requirements.txt
def read_requirements():
    with open(global_var.requirements_path) as f:
        requirements = f.read().splitlines()
        # print(requirements)
    return requirements


# Start
if __name__ == '__main__':
    print("Script Started...")
    # Start Time of Code
    start_time = time.time()

    read_requirements()

    dependencies = read_requirements()

    # Check for dependencies
    try:
        for module in dependencies:
            module_check = importlib.util.find_spec(module)  # works for python >= 3.4
            if module_check is None:
                install(module)

        print("Dependencies resolved...")

    except ImportError:
        print("There was an issue in resolving dependencies!")

    # Print Time taken to execute script
    print("CUSTOM INFO : --- Script Execution Time: %s seconds ---" % (time.time() - start_time))

