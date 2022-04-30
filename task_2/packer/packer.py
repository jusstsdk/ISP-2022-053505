import builtins
import importlib
import inspect
import types


class Packer:
    def pack(self, obj):
        """Packs any object into dict"""
        obj_dict = {}

        if type(obj) in (int, float, str, bool):
            if type(obj) == int:
                obj_dict["type"] = "int"
                obj_dict["data"] = obj
                return obj_dict
            elif type(obj) == float:
                obj_dict["type"] = "float"
                obj_dict["data"] = obj
                return obj_dict
            elif type(obj) == bool:
                obj_dict["type"] = "bool"
                obj_dict["data"] = obj
                return obj_dict
            elif type(obj) == str:
                obj_dict["type"] = "str"
                obj_dict["data"] = obj
                return obj_dict

        if type(obj) in (dict, list, tuple, set, frozenset):
            if isinstance(obj, dict):
                obj_dict["type"] = "dict"
                obj_dict["data"] = {key: self.pack(val) for key, val in obj.items()}
                return obj_dict
            if isinstance(obj, list):
                obj_dict["type"] = "list"
                obj_dict["data"] = [self.pack(el) for el in obj]
                return obj_dict
            if isinstance(obj, tuple):
                obj_dict["type"] = "tuple"
                obj_dict["data"] = [self.pack(el) for el in obj]
                return obj_dict
            if isinstance(obj, set):
                obj_dict["type"] = "set"
                obj_dict["data"] = [self.pack(el) for el in obj]
                return obj_dict
            if isinstance(obj, frozenset):
                obj_dict["type"] = "frozenset"
                obj_dict["data"] = [self.pack(el) for el in obj]
                return obj_dict
        if obj is None:
            obj_dict['type'] = 'NoneType'
            obj_dict['value'] = None
            return obj_dict
        if isinstance(obj, bytes):
            obj_dict["type"] = "bytes"
            obj_dict["data"] = [byte for byte in obj]
            return obj_dict
        if isinstance(obj, bytearray):
            obj_dict["type"] = "bytearray"
            obj_dict["data"] = [byte for byte in obj]
            return obj_dict
        if isinstance(obj, types.CodeType):
            obj_dict["type"] = "codeobject"
            obj_dict["data"] = self.pack(self.get_codeobject_attrs(obj))
            return obj_dict
        if isinstance(obj, types.FunctionType):
            obj_dict["type"] = "function"
            obj_dict["data"] = self.pack(self.pack_function(obj))
            return obj_dict
        if isinstance(obj, types.BuiltinFunctionType):
            obj_dict["type"] = "builtinfunction"
            obj_dict["data"] = self.pack(self.pack_builtin_function(obj))
            return obj_dict
        if inspect.isclass(obj):
            obj_dict["type"] = "class"
            obj_dict["data"] = self.pack(self.pack_class(obj))
            return obj_dict
        if inspect.ismodule(obj):
            obj_dict["type"] = "module"
            obj_dict["data"] = inspect.getmodule(obj).__name__
            return obj_dict
        if self.is_instance(obj):
            obj_dict["type"] = "instance"
            obj_dict["data"] = self.pack(self.pack_instance(obj))
            return obj_dict

    @staticmethod
    def get_codeobject_attrs(obj):

        if isinstance(obj, types.CodeType):
            result = {}
            for key in dir(obj):
                if key.startswith("co_"):
                    value = obj.__getattribute__(key)
                    result[key] = value
            return result

    @staticmethod
    def pack_builtin_function(obj):
        """Packs built-in function into dict"""
        result = dict()
        result["type"] = "built-in function"
        result["module"] = obj.__module__
        result["attributes"] = {"__name__": obj.__name__}
        return result

    def pack_function(self, obj):
        """Packs function into dict"""
        result = dict()
        attributes = dict()

        attributes["__name__"] = obj.__qualname__
        attributes["__defaults__"] = obj.__defaults__
        attributes["__closure__"] = obj.__closure__
        attributes["__code__"] = obj.__code__

        code_obj_dir = dir(obj.__code__)
        co_list = list()

        for item in code_obj_dir:
            if item.startswith("co_"):
                co_list.append(item)

        global_ns = dict()
        self.get_closure_globs(obj, global_ns)
        result["__globals__"] = global_ns
        result["attributes"] = attributes
        return result

    def get_closure_globs(self, obj, globs):
        if hasattr(obj, '__code__'):
            code_obj = obj.__code__
            for var in code_obj.co_consts:
                self.get_closure_globs(var, globs)
            for name in code_obj.co_names:
                if name in obj.__globals__.keys() and name != obj.__name__:
                    globs[name] = obj.__globals__[name]
                elif name in dir(builtins):
                    globs[name] = getattr(builtins, name)

    @staticmethod
    def is_instance(obj):
        if not hasattr(obj, "__dict__"):
            return False
        if inspect.isroutine(obj):
            return False
        if inspect.isclass(obj):
            return False
        if inspect.ismodule(obj):
            return False
        else:
            if not hasattr(obj, '__module__'):
                return
            mod = importlib.import_module(obj.__module__)
            if obj.__class__.__name__ in dict(
                    inspect.getmembers(mod, inspect.isclass)
            ):
                return True
            else:
                return False

    @staticmethod
    def pack_instance(obj):
        result = dict()
        result["class"] = obj.__class__
        result["dict"] = obj.__dict__
        return result

    @staticmethod
    def pack_class(obj):
        result = dict()
        result["__name__"] = obj.__name__
        result["__bases__"] = tuple(
            [base for base in obj.__bases__ if base is not object]
        )
        result["__dict__"] = dict(obj.__dict__)
        return result
