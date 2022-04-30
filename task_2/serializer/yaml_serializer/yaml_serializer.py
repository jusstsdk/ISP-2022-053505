from packer.packer import Packer
from packer.unpacker import Unpacker
from io import StringIO
from yaml import safe_dump, safe_load


class YamlSerializer:
    def __init__(self):
        self.packer = Packer()
        self.unpacker = Unpacker()

    def dump(self, obj: object, path):
        obj_dict = self.packer.pack(obj)
        with open(path, "w") as file:
            safe_dump(obj_dict, file)

    def dumps(self, obj: object):
        obj_dict = self.packer.pack(obj)
        result_string = safe_dump(obj_dict)
        return result_string

    def load(self, path):
        with open(path, "r") as file:
            obj_dict = safe_load(file)
        obj = self.unpacker.unpack(obj_dict)
        return obj

    def loads(self, obj_str: str):
        str_stream = StringIO(obj_str)
        obj_dict = safe_load(str_stream)
        obj = self.unpacker.unpack(obj_dict)
        return obj
