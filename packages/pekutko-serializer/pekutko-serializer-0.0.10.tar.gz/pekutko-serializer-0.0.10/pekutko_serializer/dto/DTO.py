from dataclasses import dataclass


@dataclass
class DTO_TYPES():
    FUNC = "func"
    CODE = "code"
    MODULE = "module"
    CLASS = "class"
    OBJ = "obj"
    DICT = "dict"
    LIST = "list"

@dataclass
class DTO():
    dto_type = "DTO_TYPE"
    name = "name"
    fields = "fields"
    path = "path"
    code = "code"
    global_names = "globals"
    base_class = "class"
    item = "__dto__list_dict_item"
