import imp
import inspect
import re
from types import CodeType, FunctionType, ModuleType

from ...dto import DTO, DTO_TYPES
from . import toml_tokens
TOKEN_TYPES = toml_tokens

class TomlParser():

    __tokens: list = []
    __container_names = []

    def _eat(self, token_types: tuple) -> tuple:
        if len(self.__tokens):
            if self.__tokens[0][0] in token_types:
                return self.__tokens.pop(0)
        return ("", "")

    def _head_token(self) -> tuple:
        if len(self.__tokens):
            return self.__tokens[0]

    def _lex(self, source: str) -> list:
        tokens = []
        while len(source) > 0:
            for token in TOKEN_TYPES.TOKEN_REGEXPS.items():
                if token[0] == TOKEN_TYPES.EOF:
                    continue
                regexp_res = re.match(token[1], source)
                if regexp_res and regexp_res.start() == 0 and len(regexp_res.group(0)):
                    source = str(
                        source[regexp_res.end()-regexp_res.start():])
                    if token[0] in (TOKEN_TYPES.STR, TOKEN_TYPES.FIELD_STR):
                        string = regexp_res.group(0)
                        tokens.append((token[0], string.replace('"', "")))
                    elif token[0] == TOKEN_TYPES.NUMBER:
                        num = regexp_res.group(0)
                        num = float(num) if "." in num else int(num)
                        tokens.append((token[0], num))
                    elif token[0] == TOKEN_TYPES.BOOL:
                        _bool = regexp_res.group(0)
                        res = True if _bool == "true" else False
                        tokens.append((token[0], res))
                    else:
                        tokens.append((token[0],))
        tokens.append((TOKEN_TYPES.EOF,))
        return tokens

    def skip_newlines(self):
        while self._head_token()[0] == TOKEN_TYPES.NEW_LINE:
            self._eat(TOKEN_TYPES.NEW_LINE)

    def _push_name(self, s: str):
        self.__container_names.append(s)

    def _pop_name(self) -> str:
        return self.__container_names.pop()

    def _parse_container_names(self, no_eat: bool = False) -> list:
        tokens_copy = [t for t in self.__tokens]
        self._eat(TOKEN_TYPES.LBRACKET)
        names = []
        while self._head_token()[0] != TOKEN_TYPES.RBRACKET:
            token = self._eat((TOKEN_TYPES.FIELD_STR, TOKEN_TYPES.POINT))
            if token[0] == TOKEN_TYPES.FIELD_STR:
                names.append(token[1])
        self._eat(TOKEN_TYPES.RBRACKET)
        self._eat(TOKEN_TYPES.NEW_LINE)
        if no_eat:
            self.__tokens = tokens_copy
        return names

    def _skip_field_name(self) -> str:
        field_key = self._eat(TOKEN_TYPES.FIELD_STR)
        self._eat(TOKEN_TYPES.ASSIGN)
        return field_key[1]

    def _parse_func_code(self) -> CodeType:
        # fields
        self._skip_field_name()
        code_dict = self._parse()
        code_dict["co_consts"] = sorted(code_dict["co_consts"], key = lambda el: str(el).find("<"))

        func_code = CodeType(
            int(code_dict["co_argcount"]),
            int(code_dict["co_posonlyargcount"]),
            int(code_dict["co_kwonlyargcount"]),
            int(code_dict["co_nlocals"]),
            int(code_dict["co_stacksize"]),
            int(code_dict["co_flags"]),
            bytes.fromhex(code_dict["co_code"]),
            tuple(code_dict["co_consts"]),
            tuple(code_dict["co_names"]),
            tuple(code_dict["co_varnames"]),
            str(code_dict["co_filename"]),
            str(code_dict["co_name"]),
            int(code_dict["co_firstlineno"]),
            bytes.fromhex(code_dict["co_lnotab"]),
            tuple(code_dict["co_freevars"]),
            tuple(code_dict["co_cellvars"]),
        )
        return func_code

    def _parse_func(self) -> any:
        # name
        self._skip_field_name()
        func_name = self._parse()
        self.skip_newlines()
        # globals
        self._skip_field_name()
        func_globals = self._parse()
        self.skip_newlines()
        # code
        self._skip_field_name()
        func_code = self._parse()
        self.skip_newlines()

        # print(func_code)

        # print("_________")
        # for c in func_code.items():
        #     print(c)
        # exit()

        func = FunctionType(func_code, func_globals, func_name)
        func.__globals__["__builtins__"] = __import__("builtins")
        return func

    # def _is_sub_list(self, extern_list: list, internal_list: list) -> bool:
    #     ex_len, in_len = len(extern_list), len(internal_list)

    def _parse_module(self) -> ModuleType:
        # name
        self._skip_field_name()
        module_name = self._parse()
        # fields
        self._skip_field_name()
        module_fields = self._parse()

        module = None
        # first case mean that module is in python std or built in
        if module_fields == None:
            module = __import__(module_name)
        else: 
            module = imp.new_module(module_name)
            for field in module_fields.items():
                setattr(module,field[0],field[1])
        return module

    def _parse_class(self) -> type:
        # name
        self._skip_field_name()
        class_name = self._parse()
        # fields
        self._skip_field_name()
        class_members_dict = self._parse()

        class_bases = (object,)
        if "__bases__" in class_members_dict:
            class_bases = tuple(class_members_dict["__bases__"])
        return type(class_name, class_bases, class_members_dict)

    def _parse_obj(self) -> object:
        # class
        self._skip_field_name()
        _class = self._parse()
        # fields
        self._skip_field_name()
        fields_dict = self._parse_dto()

        class_init = _class.__init__
        if callable(class_init):
            if class_init.__class__.__name__ == "function":
                delattr(_class, "__init__")
        obj = _class()
        obj.__init__ = class_init
        obj.__dict__ = fields_dict
        return obj

    def _parse_dict(self):
        # print(self.__container_names)
        _dict = {}
        while self._head_token()[0] not in (TOKEN_TYPES.LBRACKET, TOKEN_TYPES.EOF):
            key = self._skip_field_name()
            value = self._parse()
            _dict.update({key: value})
            self.skip_newlines()
        if self._head_token()[0] != TOKEN_TYPES.EOF:
            while self._head_token()[0] != TOKEN_TYPES.EOF:
                next_names = self._parse_container_names(no_eat=True)
                if next_names[:-1] == self.__container_names or len(self.__container_names) == 0:
                    field_name = next_names[-1:][0]
                    value = self._parse_dto()
                    _dict.update({field_name: value})
                    if self._head_token()[0] == TOKEN_TYPES.EOF:
                        break
                    self.skip_newlines()
                    next_names = self._parse_container_names(no_eat=True)
                else:
                    break
        # print(self.__container_names,"end")
        return _dict

    def _parse_list(self) -> list:
        _dict = self._parse_dict()
        return list(_dict.values())

    def _parse_primitive(self) -> any:
        token_type = self._head_token()[0]
        res = None
        if token_type == TOKEN_TYPES.NUMBER:
            res = self._eat(TOKEN_TYPES.NUMBER)[1]
        elif token_type == TOKEN_TYPES.STR:
            res = self._eat(TOKEN_TYPES.STR)[1]
        elif token_type == TOKEN_TYPES.LBRACKET:
            self._eat(TOKEN_TYPES.LBRACKET)
            self._eat(TOKEN_TYPES.RBRACKET)
            res = []
        elif token_type == TOKEN_TYPES.NULL:
            self._eat(TOKEN_TYPES.NULL)
            res = None
        elif token_type == TOKEN_TYPES.BOOL:
            res = self._eat(TOKEN_TYPES.BOOL)[1]
        self._eat(TOKEN_TYPES.NEW_LINE)
        return res

    def _parse_dto(self, global_scope: bool = False):
        self.skip_newlines()
        if not global_scope:
            names: list = self._parse_container_names()
            if len(names) >= 1:
                self._push_name(names[len(names)-1])

        dto_type_key = self._eat(TOKEN_TYPES.FIELD_STR)
        self._eat(TOKEN_TYPES.ASSIGN)
        dto_type_value = self._eat(TOKEN_TYPES.STR)
        self._eat(TOKEN_TYPES.NEW_LINE)

        res_dto = None

        if dto_type_key[1] == DTO.dto_type:
            if dto_type_value[1] == DTO_TYPES.DICT:
                res_dto = self._parse_dict()
            elif dto_type_value[1] == DTO_TYPES.LIST:
                res_dto = self._parse_list()
            elif dto_type_value[1] == DTO_TYPES.FUNC:
                res_dto = self._parse_func()
            elif dto_type_value[1] == DTO_TYPES.CODE:
                res_dto = self._parse_func_code()
            elif dto_type_value[1] == DTO_TYPES.MODULE:
                res_dto = self._parse_module()
            elif dto_type_value[1] == DTO_TYPES.CLASS:
                res_dto = self._parse_class()
            elif dto_type_value[1] == DTO_TYPES.OBJ:
                res_dto = self._parse_obj()

        if not global_scope:
            self._pop_name()

        return res_dto

    def _parse(self) -> any:
        self.skip_newlines()
        head_token_type = self._head_token()[0]
        if head_token_type == TOKEN_TYPES.FIELD_STR:
            return self._parse_dto(global_scope=True)
        elif head_token_type == TOKEN_TYPES.LBRACKET:
            # check below need to avoid empty array during parsing in parse_dto method
            if self.__tokens[1][0] != TOKEN_TYPES.RBRACKET:
                return self._parse_dto()
        return self._parse_primitive()

    def parse(self, s: str) -> any:
        self.__tokens = self._lex(s)
        # remove all space tokens
        self.__tokens = list(filter(
            lambda token: token[0] != TOKEN_TYPES.SPACE,
            self.__tokens
        ))
        return self._parse()
