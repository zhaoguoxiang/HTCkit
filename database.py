from pathlib import Path
import os


def __iter_structure(function):
    """遍历所有root_dir下的文件夹，将数据保存成为{id_0:data, id_1:data,...}"""

    def _func(self):
        d = {}
        for structure_dir in Path(self.root_dir).iterdir():
            os.chdir(structure_dir)
            data = function(self, structure_id=structure_dir.stem)
            d[structure_dir.stem] = data
        os.chdir(self.initial_dir)
        return d

    return _func


class Database:
    def __init__(self, root_dir, initial_dir=os.getcwd()) -> None:
        self.root_dir = root_dir
        self.structure_dir_list = list(Path(root_dir).iterdir())
        self.initial_dir = initial_dir

    @__iter_structure
    def func(self, structure_id):
        print(structure_id)


if __name__ == "__main__":
    data = Database("/home/dell/HTCkit/temp")
    a = data.func()
