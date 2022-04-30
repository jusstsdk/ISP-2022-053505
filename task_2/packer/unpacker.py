import importlib
import types


class Unpacker:
    @staticmethod
    def unpack_class(obj_dict):
        obj = type(obj_dict["__name__"], obj_dict["__bases__"], obj_dict["__dict__"])
        return obj

    @staticmethod
    def unpack_instance(obj_dict):
        klass = obj_dict["class"]
        obj = klass()
        for key, attr in obj_dict["dict"].items():
            setattr(obj, key, attr)
        return obj

    @staticmethod
    def unpack_codeobject(obj_dict):
        code_obj = types.CodeType(
            obj_dict["co_argcount"],
            obj_dict["co_posonlyargcount"],
            obj_dict["co_kwonlyargcount"],
            obj_dict["co_nlocals"],
            obj_dict["co_stacksize"],
            obj_dict["co_flags"],
            obj_dict["co_code"],
            obj_dict["co_consts"],
            obj_dict["co_names"],
            obj_dict["co_varnames"],
            obj_dict["co_filename"],
            obj_dict["co_name"],
            obj_dict["co_firstlineno"],
            obj_dict["co_lnotab"],
            obj_dict["co_freevars"],
            obj_dict["co_cellvars"],
        )
        return code_obj

    @staticmethod
    def unpack_function(obj_dict):
        attrs = obj_dict["attributes"]
        obj = types.FunctionType(
            code=attrs["__code__"],
            globals=obj_dict["__globals__"],
            name=attrs["__name__"],
            argdefs=attrs["__defaults__"],
            closure=attrs["__closure__"],
        )
        return obj

    @staticmethod
    def unpack_builtinfunction(obj_dict):
        module = importlib.import_module(obj_dict["module"])
        obj = getattr(module, obj_dict["attributes"]["__name__"])
        return obj

    def unpack(self, obj_dict):
        try:
            t = obj_dict["type"]
        except:
            return

        if t in ("int", "float", "bool", "str"):
            if t == "int":
                return int(obj_dict["data"])
            elif t == "float":
                return float(obj_dict["data"])
            elif t == "bool":
                return bool(obj_dict["data"])
            elif t == "str":
                return str(obj_dict["data"])

        if t in ("dict", "list", "tuple", "set", "frozenset"):
            if t == "dict":
                tmp = {key: self.unpack(val) for key, val in obj_dict["data"].items()}
                if "type" in tmp.keys():
                    if "data" in tmp.keys():
                        return self.unpack(tmp["data"])
                return tmp
            elif t == "list":
                return [self.unpack(el) for el in obj_dict["data"]]
            elif t == "tuple":
                o = [self.unpack(el) for el in obj_dict["data"]]
                return tuple(o)
            elif t == "set":
                o = [self.unpack(el) for el in obj_dict["data"]]
                return set(o)
            elif t == "frozenset":
                o = [self.unpack(el) for el in obj_dict["data"]]
                return frozenset(o)

        if t == "bytes":
            return bytes(obj_dict["data"])
        if t == "bytearray":
            return bytearray(obj_dict["data"])
        if t == "codeobject":
            obj = self.unpack_codeobject(self.unpack(obj_dict["data"]))
            return obj
        if t == "class":
            obj = self.unpack_class(self.unpack(obj_dict["data"]))
            return obj
        if t == "function":
            obj = self.unpack_function(self.unpack(obj_dict["data"]))
            return obj
        if t == "builtinfunction":
            obj = self.unpack_builtinfunction(self.unpack(obj_dict["data"]))
            return obj
        if t == "module":
            obj = importlib.import_module(obj_dict["data"])
            return obj
        if t == "instance":
            obj = self.unpack_instance(self.unpack(obj_dict["data"]))
            return obj
