import imp
import inspect
import re
from types import CodeType, FunctionType, ModuleType

from requests import head

from pekutko_serializer.dto import DTO, DTO_TYPES
import pekutko_serializer.parser.yaml.yaml_tokens as TOKEN_TYPES


class YamlParser():

    __tokens: list = []
    __cur_gaps_count: int = 0

    def _eat(self, token_types: tuple, gaps: bool = False) -> tuple:
        if gaps:
            self._skip_gaps()
        if len(self.__tokens):
            if self.__tokens[0][0] in token_types:
                return self.__tokens.pop(0)
        return ("", "")

    def _head_token(self, skip_gaps: bool = False) -> tuple:
        head = self.__tokens[0]
        if skip_gaps:
            for token in self.__tokens:
                if token[0] != TOKEN_TYPES.GAP:
                    head = token
                    break
        return head

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

    def _dump_tokens(self):
        for token in self.__tokens:
            print(token)

    def _skip_field_name(self) -> str:
        self._skip_gaps()
        field_key = self._eat(TOKEN_TYPES.FIELD_STR)
        self._eat(TOKEN_TYPES.COLON)
        self._skip_gaps()
        return field_key[1]

    def _peek_gaps_count(self) -> int:
        for i in range(len(self.__tokens)):
            if self.__tokens[i][0] != TOKEN_TYPES.GAP:
                return i

    def _skip_gaps(self) -> int:
        i = 0
        while self._head_token()[0] == TOKEN_TYPES.GAP:
            self._eat(TOKEN_TYPES.GAP)
            i += 1
        return i

    def _push_gap(self):
        self.__cur_gaps_count += 1

    def _pop_gap(self):
        self.__cur_gaps_count -= 1

    def _parse_func_code(self) -> CodeType:
        self._push_gap()
        # fields
        self._skip_field_name()
        code_dict = self._parse()

        self._pop_gap()

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
        self._push_gap()
        # name
        self._skip_field_name()
        func_name = self._parse()
        # globals
        self._skip_field_name()
        func_globals = self._parse()
        # code
        self._skip_field_name()
        func_code = self._parse()
        
        # print(func_name, func_globals, func_code)
        # exit()
        self._pop_gap()
        # print()
        # exit()

        func = FunctionType(func_code, func_globals, func_name)
        func.__globals__["__builtins__"] = __import__("builtins")
        return func

    def _parse_module(self) -> ModuleType:
        self._push_gap()
        # name
        self._skip_field_name()
        module_name = self._parse()
        # fields
        self._skip_field_name()
        module_fields = self._parse()

        self._pop_gap()

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
        self._push_gap()
        # name
        self._skip_field_name()
        class_name = self._parse()
        # fields
        self._skip_field_name()
        class_members_dict = self._parse()

        # print(class_members_dict)
        # exit()
        self._pop_gap()

        class_bases = (object,)
        if "__bases__" in class_members_dict:
            class_bases = tuple(class_members_dict["__bases__"])
        return type(class_name, class_bases, class_members_dict)

    def _parse_obj(self) -> object:
        self._push_gap()
        # class
        self._skip_field_name()
        _class = self._parse()
        # fields
        self._skip_field_name()
        fields_dict = self._parse()
        self._pop_gap()

        class_init = _class.__init__
        if callable(class_init):
            if class_init.__class__.__name__ == "function":
                delattr(_class, "__init__")
        obj = _class()
        obj.__init__ = class_init
        obj.__dict__ = fields_dict
        return obj

    def _parse_dict(self):
        _dict = {}
        start_gaps_count = self.__cur_gaps_count
        self._push_gap()
        while self._peek_gaps_count() == start_gaps_count and self._head_token()[0] != TOKEN_TYPES.EOF:
            co_key = self._skip_field_name()
            co_value = self._parse()
            _dict.update({co_key: co_value})
        self._pop_gap()
        return _dict

    def _parse_list(self) -> list:
        _list = []
        start_gaps_count = self.__cur_gaps_count
        self._push_gap()
        while self._peek_gaps_count() == start_gaps_count and self._head_token()[0] != TOKEN_TYPES.EOF:
            self._skip_gaps()
            self._eat(TOKEN_TYPES.ARR_DASH)
            element = self._parse()
            _list.append(element)
        self._pop_gap()
        return _list

    def _parse_primitive(self) -> any:
        token_type = self._head_token()[0]
        res = None
        if token_type == TOKEN_TYPES.NUMBER:
            res = self._eat(TOKEN_TYPES.NUMBER)[1]
        elif token_type == TOKEN_TYPES.STR:
            res = self._eat(TOKEN_TYPES.STR)[1]
        elif token_type == TOKEN_TYPES.BOOL:
            res = self._eat(TOKEN_TYPES.BOOL)[1]
        elif token_type == TOKEN_TYPES.NULL:
            self._eat(TOKEN_TYPES.NULL)
            res = None
        self._eat(TOKEN_TYPES.NEW_LINE)
        return res

    def _parse_dto(self):

        dto_type_key = self._eat(TOKEN_TYPES.FIELD_STR, gaps=True)
        self._eat(TOKEN_TYPES.COLON)
        dto_type_value = self._eat(TOKEN_TYPES.STR)
        self._eat(TOKEN_TYPES.NEW_LINE)

        res_dto = None

        # self._push_gap()
        if dto_type_key[1] == DTO.dto_type:
            if dto_type_value[1] == DTO_TYPES.DICT:
                res_dto = self._parse_dict()
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
        # self._pop_gap()
        return res_dto

    def _parse(self) -> any:
        head_token_type = self._head_token()[0]
        # print(head_token_type)
        if head_token_type == TOKEN_TYPES.LBRACKET:
            self._eat(TOKEN_TYPES.LBRACKET)
            self._eat(TOKEN_TYPES.RBRACKET)
            self._eat(TOKEN_TYPES.NEW_LINE)
            return []
        elif head_token_type in (TOKEN_TYPES.NEW_LINE, TOKEN_TYPES.FIELD_STR):
            self._eat(TOKEN_TYPES.NEW_LINE)
            if self._head_token(skip_gaps=True)[0] == TOKEN_TYPES.ARR_DASH:
                return self._parse_list()
            self._skip_gaps()
            return self._parse_dto()
        return self._parse_primitive()

    def parse(self, s: str) -> any:
        self.__tokens = self._lex(s)
        return self._parse()
