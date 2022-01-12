import os
import shutil
from pathlib import Path


def initialize(root_dir):
    run_dir = os.getcwd()
    os.chdir(root_dir)
    for structure in Path(root_dir).iterdir():
        if not structure.is_dir():
            os.mkdir(structure.stem)
            shutil.move(structure.name,structure.stem)

    os.chdir(run_dir)

if __name__ == "__main__":
    initialize("/home/dell/HTCkit/temp")