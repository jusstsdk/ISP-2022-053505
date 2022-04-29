from packer.packer import Packer
from packer.unpacker import Unpacker
import toml


class TomlSerializer:
    def __init__(self):
        self.packer = Packer()
        self.unpacker = Unpacker()

    def dump(self, obj: object, path):
        obj_dict = self.packer.pack(obj)
        with open(path, "w") as file:
            toml.dump(obj_dict, file)

    def dumps(self, obj: object):
        obj_dict = self.packer.pack(obj)
        return toml.dumps(obj_dict)

    def load(self, path):
        with open(path, "r") as file:
            obj_dict = toml.load(file)
        obj = self.unpacker.unpack(obj_dict)
        return obj

    def loads(self, obj_str: str):
        obj_dict = toml.loads(obj_str)
        return self.unpacker.unpack(obj_dict)
