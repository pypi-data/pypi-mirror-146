NEW_LINE = "newline"
GAP = "gap"
LBRACKET = "lbracket"
RBRACKET = "rbracket"
STR = "str"
FIELD_STR = "fieldstr"
ARR_DASH = "arrdash"
NUMBER = "number"
BOOL = "bool"
NULL = "null"
COLON = "colon"
EOF = "EOF"

TOKEN_REGEXPS = {
    NEW_LINE: r"\n",
    GAP: r"\s\s",
    NULL: r'null',
    COLON: r":\s",
    LBRACKET: "\\[",
    RBRACKET: "\\]",
    NUMBER: r'([0-9]*[.])?[0-9]+',
    BOOL: r'^(?:tru|fals)e',
    STR: r'"[^"]*"',
    FIELD_STR: r'[A-Za-z0-9\_]*',
    ARR_DASH: r'-\s', 
    EOF: "EOF"
}