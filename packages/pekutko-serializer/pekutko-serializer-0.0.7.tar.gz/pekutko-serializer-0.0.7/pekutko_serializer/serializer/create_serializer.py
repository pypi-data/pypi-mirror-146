from .BaseSerializer import BaseSerializer
from .json.JsonSerializer import JsonSerializer
from .toml.TomlSerializer import TomlSerializer
from .yaml.YamlSerializer import YamlSerializer


SERAILIZERS_MAP = {
    "json": JsonSerializer,
    "toml": TomlSerializer,
    "yaml": YamlSerializer
}

def create_serializer(exten_name: str) -> BaseSerializer:
    if exten_name in SERAILIZERS_MAP:
        return SERAILIZERS_MAP[exten_name]()
    else:
        return None