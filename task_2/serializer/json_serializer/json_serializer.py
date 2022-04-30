from packer.packer import Packer
from packer.unpacker import Unpacker
from serializer.json_serializer import json_parser as json


class JsonSerializer:
    def __init__(self):
        self.packer = Packer()
        self.unpacker = Unpacker()

    def dump(self, obj: object, path):
        obj_dict = self.packer.pack(obj)
        with open(path, "w") as file:
            json.dump(obj_dict, fp=file)

    def dumps(self, obj: object):
        obj_dict = self.packer.pack(obj)
        result_string = json.dumps(obj_dict)
        return result_string

    def load(self, path):
        with open(path, "r") as file:
            obj_dict = json.load(file)
        obj = self.unpacker.unpack(obj_dict)
        return obj

    def loads(self, obj_str: str):
        obj_dict = json.loads(obj_str)
        obj = self.unpacker.unpack(obj_dict)
        return obj
