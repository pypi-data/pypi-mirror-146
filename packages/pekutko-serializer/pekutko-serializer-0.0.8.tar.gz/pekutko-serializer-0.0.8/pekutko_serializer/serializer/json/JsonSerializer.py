from ast import Module
import imp
import inspect
from types import BuiltinFunctionType, CodeType, GetSetDescriptorType, MappingProxyType, MethodDescriptorType, ModuleType, WrapperDescriptorType
from ..BaseSerializer import BaseSerializer
from ...parser.json.JsonParser import JsonParser
from ...dto import DTO, DTO_TYPES

from ... import utils

class JsonSerializer(BaseSerializer):
    __res_str = ""
    __parser = None

    def __init__(self):
        super().__init__()
        self.__parser = JsonParser()

    def dumps(self, obj: any) -> str:
        self.__res_str = ""
        self._visit(obj)
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

    def _visit_func_globals(self, func):
        actual_globals = utils.get_actual_func_globals(func)
        self._visit(actual_globals)

    def _visit_func_code(self, _code: CodeType):
        self._put(f'"{DTO.dto_type}": "{DTO_TYPES.CODE}",')
        self._put(f'"{DTO.fields}":')
        code_dict = utils.get_actual_code_fields(_code)
        self._visit(code_dict)

    def _visit_func(self, func):
        self._put(f'"{DTO.dto_type}": "{DTO_TYPES.FUNC}",')
        self._put(f'"{DTO.name}": "{func.__name__}",')
        self._put(f'"{DTO.global_names}": ')
        self._visit_func_globals(func)
        self._put(',')
        self._put(f'"{DTO.code}": ')
        self._visit(func.__code__)

    def _visit_module(self, module):
        self._put(f'"{DTO.dto_type}": "{DTO_TYPES.MODULE}",')
        self._put(f'"{DTO.name}": "{module.__name__}",')
        self._put(f'"{DTO.fields}": ')
        if utils.is_std_lib_module(module):
            self._visit(None)
        else:
            module_fields = utils.get_actual_module_fields(module)
            self._visit(module_fields)

    def _visit_class(self, _class):
        self._put(f'"{DTO.dto_type}": "{DTO_TYPES.CLASS}",')
        self._put(f'"{DTO.name}": "{_class.__name__}",')
        self._put(f'"{DTO.fields}": ')
        fields_dict = utils.get_actual_class_fields(_class)
        self._visit(fields_dict)

    def _visit_obj(self, obj):
        # print(obj)
        self._put(f'"{DTO.dto_type}": "{DTO_TYPES.OBJ}",')
        self._put(f'"{DTO.base_class}": ')
        self._visit(obj.__class__)
        self._put(",")
        self._put(f'"{DTO.fields}": ')
        self._visit(obj.__dict__)

    def _visit_dict(self, _dict: dict):
        self._put(f'"{DTO.dto_type}": "{DTO_TYPES.DICT}"')
        if len(_dict.items()) >= 1:
            self._put(",")
        is_first = True
        for item in _dict.items():
            if not is_first:
                self._put(',')
            self._put(f'"{item[0]}": ')
            self._visit(item[1])
            is_first = False

    def _visit_primitive(self, prim_obj):
        _type = type(prim_obj)
        if _type in (int, float):
            self._put(f'{prim_obj}')
        elif _type == str:
            self._put(f'"{prim_obj}"')
        elif _type == bool:
            val = "true" if prim_obj else "false"
            self._put(f'{val}')
        elif _type in (list, tuple):
            self._put('[')
            for i, obj in enumerate(prim_obj):
                if i != 0:
                    self._put(",")
                self._visit(obj)
            self._put(']')
        elif _type == bytes:
            encoded = prim_obj.hex()
            self._put(f'"{encoded}"')

    def _visit(self, obj):
        if type(obj) in (int, float, str, bool, bytes, tuple, list):
            self._visit_primitive(obj)
        elif obj == None:
            self._put('null')
        else:
            self._put('{')
            if type(obj) == dict:
                self._visit_dict(obj)
            elif type(obj) == CodeType:
                self._visit_func_code(obj)
            elif type(obj) == ModuleType:
                self._visit_module(obj)
            elif inspect.isclass(obj):
                self._visit_class(obj)
            elif callable(obj):
                self._visit_func(obj)
            elif isinstance(obj, object):
                self._visit_obj(obj)
            self._put('}')
