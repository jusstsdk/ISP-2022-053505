from serializer.json_serializer.json_serializer import JsonSerializer
from serializer.toml_serializer.toml_serializer import TomlSerializer
from serializer.yaml_serializer.yaml_serializer import YamlSerializer


class SerializerFactory:
    @staticmethod
    def create_serializer(extension):
        if extension.lower() == "json":
            return JsonSerializer()
        elif extension.lower() == "toml":
            return TomlSerializer()
        elif extension.lower() == "yaml":
            return YamlSerializer()
