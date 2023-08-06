from enum import Enum


class DropStyle(Enum):
    """
    Represents the three approaches to handling the dropping of objects
    """
    # No objects will be dropped, User sql scripts will take care of the dropping of objects
    NONE = 1

    # The schema will be dropped and recreated before models are generated. This method prevents any objects from
    # accumulating in the schema
    SCHEMA = 2

    # The table will be dropped before the model is generated
    TABLE = 3


class ConfigFormats(Enum):
    # cfg/ini format
    INI = 'ini'

    # JSON format
    JSON = 'json'

    # TOML format
    TOML = 'toml'

    # YAML format
    YAML = 'yaml'
