from pathlib import Path
import os
import cclib


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


def iter_structure(function):
    """遍历所有root_dir下的文件夹，将数据保存成为{id_0:data, id_1:data,...}"""

    def _func(self):
        d = {}
        for structure_dir in Path(self.root_dir).iterdir():
            os.chdir(structure_dir)
            data = function(self)
            d[structure_dir.stem] = data
        os.chdir(self.initial_dir)
        return d

    return _func


class Database:
    def __init__(self, root_dir, initial_dir=os.getcwd()) -> None:
        self.root_dir = root_dir
        self.structure_dir_list = list(Path(root_dir).iterdir())
        self.initial_dir = initial_dir

    @iter_structure
    def func(self, structure_id):
        print(structure_id)

    @property
    @iter_structure
    def opt_metod(self):
        """this will return the 4th line in the opt.gjf file"""

        with open("opt.gjf", "r") as f:
            lines = f.read().split()
        if "/genecp" in lines[3]:
            t = 0
            for idx, line in enumerate(lines[7:]):
                if line is "":
                    t = idx
                    break
            return lines[3], "\n".join(lines[t + 1 :])
        else:
            return lines[3]

    @property
    @iter_structure
    def egap(self):
        data = cclib.io.ccread("opt.log")
        mo = data.moenergies
        homo_id = data.homos
        if len(mo) == 1:
            homo = mo[0][homo_id[0]]
            lumo = mo[0][homo_id[0] + 1]
            return lumo - homo, homo, lumo
        elif len(mo) == 2:
            homo_0 = mo[0][homo_id[0]]
            lumo_0 = mo[0][homo_id[0] + 1]
            egap_0 = lumo_0 - homo_0

            homo_1 = mo[1][homo_id[1]]
            lumo_1 = mo[1][homo_id[1] + 1]
            egap_1 = lumo_1 - homo_1

            if egap_0 < egap_1:
                return egap_0, homo_0, lumo_0
            else:
                return egap_1, homo_1, lumo_1

    @property
    @iter_structure
    def dipole_momemt(self):
        data = cclib.io.ccread("opt.log")
        monents = data.moment
        return monents[1]

    @property
    @iter_structure
    def gamma_method(self):
        # todo this need to be tested
        with open("gamma.gjf", "r") as f:
            lines = f.read().split()
        if "/genecp" in lines[3]:
            t = 0
            i = 0
            for idx, line in enumerate(lines[7:]):
                if line is "":
                    i += 1
                    t = idx
                    if i == 2:
                        break
            return lines[3], "\n".join(lines[t + 1 :])
        else:
            return lines[3]        

if __name__ == "__main__":
    data = Database("/home/dell/HTCkit/temp")
    a = data.func()
