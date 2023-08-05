import inspect
import re
from types import BuiltinFunctionType, CodeType, GetSetDescriptorType, MappingProxyType, MethodDescriptorType, ModuleType, WrapperDescriptorType
from ... import utils
from ...parser.toml.TomlParser import TomlParser
from ...dto import DTO, DTO_TYPES
from ..BaseSerializer import BaseSerializer


class TomlSerializer(BaseSerializer):
    __res_str = ""
    __container_names = []
    __parser = None

    def __init__(self):
        super().__init__()
        self.__parser = TomlParser()

    def dumps(self, obj: any) -> str:
        self.__res_str = ""
        self._visit(obj)
        # replace all repeated new lines
        self.__res_str = re.sub(r"(\n)\1{2,}", "\n\n", self.__res_str)
        return self.__res_str

    def dump(self, obj: any, file_path: str):
        with open(file_path, "w") as file:
            _str = self.dumps(obj)
            file.write(_str)

    def loads(self, source: str) -> any:
        return self.__parser.parse(source)

    def load(self, file_path: str) -> any:
        obj = None
        with open(file_path) as file:
            _str = file.read()
            obj = self.loads(_str)
        return obj

    def _put(self, s: str):
        self.__res_str += s

    def _push_name(self, s: str):
        self.__container_names.append(s)

    def _pop_name(self) -> str:
        return self.__container_names.pop()

    def _get_concat_name(self) -> str:
        return (".".join(self.__container_names))[1:]

    def _is_primitive_type(self, obj: any) -> bool:
        _type = type(obj)
        if _type in (int, float, str, bool, bytes) or obj == None:
            return True
        elif _type in (tuple, list):
            if len(obj) >= 1:
                # return all(self._is_primitive_type(obj[i])==True for i in range(len(obj)))
                return False
            else:
                return True
        return False

    def _divide_dict_by_primitive(self, _dict: dict) -> tuple:
        prim_dict = {}
        complex_dict = {}
        for item in _dict.items():
            if self._is_primitive_type(item[1]):
                prim_dict.update({item[0]: item[1]})
            else:
                complex_dict.update({item[0]: item[1]})
        return prim_dict, complex_dict

    def _divide_list_by_primitive(self, _list: list) -> tuple:
        prim_list = []
        complex_list = []
        for item in _list:
            if self._is_primitive_type(item):
                prim_list.append(item)
            else:
                complex_list.append(item)
        return prim_list, complex_list

    def _visit_func_globals(self, func):
        actual_globals = utils.get_actual_func_globals(func)
        self._visit(actual_globals, DTO.global_names)

    def _visit_func_code(self, func):
        self._put(f'{DTO.dto_type} = "{DTO_TYPES.CODE}"\n\n')
        code_dict = utils.get_actual_code_fields(func)
        self._visit(code_dict, DTO.fields)

    def _visit_func(self, func):
        self._put(f'{DTO.dto_type} = "{DTO_TYPES.FUNC}"\n')
        self._put(f'{DTO.name} = "{func.__name__}"\n\n')
        self._visit_func_globals(func)
        self._visit(func.__code__, DTO.code)
        # exit()

    def _visit_module(self, module):
        self._put(f'{DTO.dto_type} = "{DTO_TYPES.MODULE}"\n')
        self._put(f'{DTO.name} = "{module.__name__}"\n')
        if utils.is_std_lib_module(module):
            self._put(f'{DTO.fields} = ')
            self._visit(None)
            self._put("\n")
        else:
            self._put("\n")
            module_fields = utils.get_actual_module_fields(module)
            self._visit(module_fields, DTO.fields)

    def _visit_class(self, _class):
        self._put(f'{DTO.dto_type} = "{DTO_TYPES.CLASS}"\n')
        self._put(f'{DTO.name} = "{_class.__name__}"\n\n')
        # self._put(f'"{DTO.fields}": ')
        fields_dict = utils.get_actual_class_fields(_class)
        self._visit(fields_dict, DTO.fields)

    def _visit_obj(self, obj):
        # print(obj)
        self._put(f'{DTO.dto_type} =  "{DTO_TYPES.OBJ}"\n\n')
        self._visit(obj.__class__, DTO.base_class)
        self._visit(obj.__dict__, DTO.fields)

    def _visit_dict(self, _dict: dict):
        # sorting dict to set primitive fields at the begining
        prim_dict, complex_dict = self._divide_dict_by_primitive(_dict)

        self._put(f'{DTO.dto_type} = "{DTO_TYPES.DICT}"\n')

        # print(prim_dict, complex_dict)
        # exit()

        for prim in prim_dict.items():
            self._put(f'{prim[0]} = ')
            self._visit(prim[1])
            self._put("\n")

        self._put("\n")

        for comp in complex_dict.items():
            self._visit(comp[1], comp[0])
            self._put("\n")

    def _visit_primitive(self, prim_obj):
        _type = type(prim_obj)
        if _type in (int, float):
            self._put(f'{prim_obj}')
        elif _type == str:
            self._put(f'"{prim_obj}"')
        elif _type == bool:
            val = "true" if prim_obj else "false"
            self._put(f'{val}')
        elif prim_obj == None:
            self._put("{}")
        elif type(prim_obj) in (tuple, list) and len(prim_obj) == 0:
            self._put("[]")
            return
        elif _type == bytes:
            encoded = prim_obj.hex()
            self._put(f'"{encoded}"')

    def _visit_list(self, _list: any):
        prim_list, complex_list = self._divide_list_by_primitive(_list)
        self._put(f'{DTO.dto_type} = "{DTO_TYPES.LIST}"\n')
        i = 0
        for prim in prim_list:
            self._put(f'{DTO.item}{i} = ')
            self._visit(prim)
            self._put("\n")
            i += 1
        self._put("\n")
        for comp in complex_list:
            self._visit(comp, f'{DTO.item}{i}')
            self._put("\n")
            i += 1

    def _visit_complex(self, comp_obj: any, container_name: str):
        self._push_name(container_name)
        name = self._get_concat_name()
        if len(self.__container_names) > 1:
            self._put(f'[{name}]\n')
        if type(comp_obj) == dict:
            self._visit_dict(comp_obj)
        elif type(comp_obj) in (tuple, list):
            self._visit_list(comp_obj)
        elif type(comp_obj) == ModuleType:
            self._visit_module(comp_obj)
        elif inspect.isclass(comp_obj):
            self._visit_class(comp_obj)
        elif type(comp_obj) == CodeType:
            self._visit_func_code(comp_obj)
        elif callable(comp_obj):
            self._visit_func(comp_obj)
        elif isinstance(comp_obj, object):
            self._visit_obj(comp_obj)

        self._pop_name()

    def _visit(self, obj, new_name: str = ""):
        if self._is_primitive_type(obj):
            self._visit_primitive(obj)
        else:
            self._visit_complex(obj, new_name)
