import unittest
from serializer.serializer_factory import SerializerFactory
from serializer.json_serializer.json_serializer import JsonSerializer
from serializer.toml_serializer.toml_serializer import TomlSerializer
from serializer.yaml_serializer.yaml_serializer import YamlSerializer
import testing_things


class TestClass(unittest.TestCase):

    def setUp(self):
        self.to_toml_serializer = SerializerFactory.create_serializer("toml")
        self.to_yaml_serializer = SerializerFactory.create_serializer("yaml")
        self.to_json_serializer = SerializerFactory.create_serializer("json")

    def test_f_yaml(self):
        self.to_yaml_serializer.dump(testing_things.f, "test.yaml")
        unpacked_f = self.to_yaml_serializer.load("test.yaml")
        self.assertEqual(testing_things.f(3), unpacked_f(3))

    def test_add_yaml(self):
        self.to_yaml_serializer.dump(testing_things.add, "test.yaml")
        unpacked_add = self.to_yaml_serializer.load("test.yaml")
        self.assertEqual(testing_things.add(), unpacked_add())

    def test_classes(self):
        ser = self.to_json_serializer.dumps(testing_things.cls1)
        unpacked_class = self.to_json_serializer.loads(ser)
        self.assertEqual(unpacked_class.__bases__[0].__name__,
                         testing_things.cls1.__bases__[0].__name__)

    def test_class_object(self):
        self.to_json_serializer.dump(testing_things.A, "test.json")
        unpacked_a = self.to_json_serializer.load("test.json")
        a1 = testing_things.A("a")
        a2 = unpacked_a("a")
        self.assertEqual(a1, a2)

    def test_json_creator(self):
        ser = self.to_json_serializer
        assert isinstance(ser, JsonSerializer)

    def test_yaml_creator(self):
        ser = self.to_yaml_serializer
        assert isinstance(ser, YamlSerializer)

    def test_toml_creator(self):
        ser = self.to_toml_serializer
        assert isinstance(ser, TomlSerializer)

    def test_set(self):
        ser = self.to_json_serializer.dumps(testing_things.set1)
        unpacked_set = self.to_json_serializer.loads(ser)
        self.assertEqual(testing_things.set1, unpacked_set)

    def test_frozenset(self):
        ser = self.to_yaml_serializer.dumps(testing_things.frzset1)
        unpacked_frzset = self.to_yaml_serializer.loads(ser)
        self.assertEqual(testing_things.frzset1, unpacked_frzset)

    def test_bytes(self):
        ser = self.to_toml_serializer.dumps(testing_things.bytes1)
        unpacked_bytes = self.to_toml_serializer.loads(ser)
        self.assertEqual(unpacked_bytes, testing_things.bytes1)

    def test_bytearr(self):
        ser = self.to_json_serializer.dumps(testing_things.bytearr1)
        unpacked_bytearr = self.to_json_serializer.loads(ser)
        self.assertEqual(unpacked_bytearr, testing_things.bytearr1)

    def test_bool(self):
        ser = self.to_json_serializer.dumps(testing_things.bool1)
        unpacked_bool = self.to_json_serializer.loads(ser)
        self.assertEqual(unpacked_bool, testing_things.bool1)

    def test_foo(self):
        self.to_toml_serializer.dump(testing_things.foo(testing_things.lst1), "test.toml")
        unpacked_foo = self.to_toml_serializer.load("test.toml")
        self.assertEqual(testing_things.foo(testing_things.lst1), unpacked_foo)

    def test_builtin(self):
        self.to_toml_serializer.dump(testing_things.bltfunc, "test.toml")
        unpacked_blt = self.to_toml_serializer.load("test.toml")
        self.assertEqual(testing_things.bltfunc, unpacked_blt)

    def test_lambda(self):
        ser = self.to_json_serializer.dumps(testing_things.power)
        unpacker_power = self.to_json_serializer.loads(ser)
        self.assertEqual(testing_things.power(2, 3), unpacker_power(2, 3))

    def test_file_io(self):
        self.to_json_serializer.dump(testing_things.mul, "test.json")
        json_obj = self.to_json_serializer.load("test.json")
        self.assertEqual(json_obj(2, 3), testing_things.mul(2, 3))
