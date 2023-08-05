import inspect
import re
from types import BuiltinFunctionType, CodeType, GetSetDescriptorType, MappingProxyType, MethodDescriptorType, ModuleType, WrapperDescriptorType

from ... import utils
from ...dto import DTO, DTO_TYPES

from ..BaseSerializer import BaseSerializer
from ...parser.yaml import YamlParser


class YamlSerializer(BaseSerializer):
    __res_str = ""
    __gaps = []
    __gaps_blocked = False
    __parser = None

    def __init__(self):
        super().__init__()
        self.__parser = YamlParser()

    def dumps(self, obj: any) -> str:
        self.__res_str = ""
        self._visit(obj, first_call=True)
        # replace all repeated new lines
        self.__res_str = re.sub(r"(\n)\1{1,}", "\n", self.__res_str)
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

    def _put(self, s: str, gaps: bool = False):
        if gaps and not self.__gaps_blocked:
            self.__res_str += "".join(self.__gaps)
        self.__res_str += s
        self.__gaps_blocked = False

    def _block_gaps(self):
        self.__gaps_blocked = True

    def _push_gap(self, gap: str = "  "):
        self.__gaps.append(gap)

    def _pop_gap(self):
        return self.__gaps.pop()

    def _visit_func_globals(self, func):
        actual_globals = utils.get_actual_func_globals(func)
        self._visit(actual_globals)

    def _visit_func_code(self, _code):
        self._put(f'{DTO.dto_type}: "{DTO_TYPES.CODE}"\n', gaps=True)
        self._put(f'{DTO.fields}:', gaps=True)
        code_dict = utils.get_actual_code_fields(_code)
        self._visit(code_dict)

    def _visit_func(self, func):
        self._put(f'{DTO.dto_type}: "{DTO_TYPES.FUNC}"\n', gaps=True)
        self._put(f'{DTO.name}: "{func.__name__}"\n', gaps=True)
        self._put(f'{DTO.global_names}:', gaps=True)
        self._visit_func_globals(func)
        self._put(f'{DTO.code}: ', gaps=True)
        self._visit(func.__code__)

    def _visit_module(self, module):
        self._put(f'{DTO.dto_type}: "{DTO_TYPES.MODULE}"\n', gaps=True)
        self._put(f'{DTO.name}: "{module.__name__}"\n', gaps=True)
        self._put(f'{DTO.fields}: ', gaps=True)
        if utils.is_std_lib_module(module):
            self._visit(None)
        else:
            module_fields = utils.get_actual_module_fields(module)
            self._visit(module_fields)

    def _visit_class(self, _class):
        self._put(f'{DTO.dto_type}: "{DTO_TYPES.CLASS}"\n', gaps=True)
        self._put(f'{DTO.name}: "{_class.__name__}"\n', gaps=True)
        self._put(f'{DTO.fields}:', gaps=True)
        mems = inspect.getmembers(_class)
        fields_dict = utils.get_actual_class_fields(_class)
        self._visit(fields_dict)

    def _visit_obj(self, obj):
        self._put(f'{DTO.dto_type}: "{DTO_TYPES.OBJ}"\n', gaps=True)
        self._put(f'{DTO.base_class}:', gaps=True)
        self._visit(obj.__class__)
        self._put(f'{DTO.fields}:', gaps=True)
        self._visit(obj.__dict__)

    def _visit_dict(self, _dict: dict):
        self._put(f'{DTO.dto_type}: "{DTO_TYPES.DICT}"\n', gaps=True)
        for item in _dict.items():
            self._put(f'{item[0]}: ', gaps=True)
            # self._push_gap()
            self._visit(item[1])
            self._put("\n")
            # self._pop_gap()

    def _visit_list(self, _list: list):
        if len(_list) >= 1:
            for item in _list:
                self._put("- ", gaps=True)
                if not self._is_primitive_type(item):
                    self._block_gaps()
                self._visit(item, new_line=False)
                self._put("\n")
        else:
            self.__res_str = self.__res_str[:-1]
            self._put("[]")

    def _is_primitive_type(self, obj: any):
        return type(obj) in (int, float, str, bool, bytes)

    def _visit_primitive(self, prim_obj):
        _type = type(prim_obj)
        if _type in (int, float):
            self._put(f'{prim_obj}')
        elif _type == str:
            self._put(f'"{prim_obj}"')
        elif _type == bool:
            val = "true" if prim_obj else "false"
            self._put(f'{val}')
        elif _type == bytes:
            encoded = prim_obj.hex()
            self._put(f'"{encoded}"')

    def _visit(self, obj: any, new_line: bool = True, first_call: bool = False):
        self._push_gap() if not first_call else None

        if self._is_primitive_type(obj):
            self._visit_primitive(obj)
        elif obj == None:
            self._put('null')
        else:
            if len(self.__gaps) >= 1 and new_line:
                self._put("\n")
            if type(obj) == dict:
                self._visit_dict(obj)
            elif type(obj) in (tuple, list):
                self._visit_list(list(obj))
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
        self._pop_gap() if not first_call else None
