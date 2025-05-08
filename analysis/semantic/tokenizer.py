# ash_tokenizer.py

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"


class Tokenizer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None

    def _peek(self):
        return self.source[self.position + 1] if self.position + 1 < len(self.source) else ""

    def select_next(self):
        while self.position < len(self.source) and self.source[self.position].isspace():
            self.position += 1

        if self.position >= len(self.source):
            self.next = Token("EOF", None)
            return

        char = self.source[self.position]

        # Match multi-char patterns
        if char == "=" and self._peek() == "=":
            self.position += 2
            self.next = Token("EQ", "==")
            return
        if char == "!" and self._peek() == "=":
            self.position += 2
            self.next = Token("NEQ", "!=")
            return
        if char == ">" and self._peek() == "=":
            self.position += 2
            self.next = Token("GTE", ">=")
            return
        if char == "<" and self._peek() == "=":
            self.position += 2
            self.next = Token("LTE", "<=")
            return
        if char == "." and self._peek() == ".":
            self.position += 2
            self.next = Token("DOTDOT", "..")
            return

        # Command capture: !(...)
        if char == "!" and self._peek() == "(":
            end = self.source.find(")", self.position)
            if end == -1:
                raise Exception("Unterminated command expression")
            content = self.source[self.position + 2:end]
            self.position = end + 1
            self.next = Token("BANG_EXPR", content)
            return

        # Inline shell command: !some text;
        if char == "!":
            start = self.position + 1
            end = start
            while end < len(self.source) and self.source[end] not in ["\n", ";"]:
                end += 1
            content = self.source[start:end]
            self.position = end
            self.next = Token("BANG_LINE", content)
            return

        if char.isdigit():
            num = ""
            while self.position < len(self.source) and self.source[self.position].isdigit():
                num += self.source[self.position]
                self.position += 1
            self.next = Token("INT", int(num))
            return

        if char == "\"":
            self.position += 1
            string = ""
            while self.position < len(self.source) and self.source[self.position] != "\"":
                string += self.source[self.position]
                self.position += 1
            if self.position >= len(self.source):
                raise Exception("Unterminated string literal")
            self.position += 1
            self.next = Token("STRING", string)
            return

        if char.isalpha() or char == "_":
            ident = ""
            while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == "_"):
                ident += self.source[self.position]
                self.position += 1

            keywords = {
                "let": "LET",
                "function": "FUNCTION",
                "if": "IF",
                "else": "ELSE",
                "for": "FOR",
                "while": "WHILE",
                "return": "RETURN",
                "echo": "ECHO_KW",
                "read": "READ",
                "in": "IN",
                "int": "INT_TYPE",
                "string": "STRING_TYPE",
                "bool": "BOOL_TYPE",
                "void": "VOID_TYPE",
                "true": "BOOL",
                "false": "BOOL"
            }

            if ident in keywords:
                val = True if ident == "true" else False if ident == "false" else ident
                self.next = Token(keywords[ident], val)
            else:
                self.next = Token("IDENTIFIER", ident)
            return

        single_tokens = {
            "=": "ASSIGN",
            "+": "PLUS",
            "-": "MINUS",
            "*": "MUL",
            "/": "DIV",
            "%": "MOD",
            "(": "LPAREN",
            ")": "RPAREN",
            "{": "LBRACE",
            "}": "RBRACE",
            ";": "SEMI",
            ":": "COLON",
            ",": "COMMA",
            "<": "LT",
            ">": "GT"
        }

        if char in single_tokens:
            self.next = Token(single_tokens[char], char)
            self.position += 1
            return

        raise Exception(f"Invalid character: {char}")

    def all_tokens(self):
        tokens = []
        self.select_next()
        while self.next.type != "EOF":
            tokens.append(self.next)
            self.select_next()
        tokens.append(self.next)
        return tokens
