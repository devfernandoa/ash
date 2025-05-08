from tokenizer import Tokenizer
from nodes import *

class AshParser:
    def __init__(self, source_code):
        self.tokenizer = Tokenizer(source_code)
        self.tokenizer.select_next()

    def parse(self):
        return self.parse_program()

    def parse_program(self):
        items = []
        while self.tokenizer.next.type != "EOF":
            if self.tokenizer.next.type in {"INT_TYPE", "STRING_TYPE", "BOOL_TYPE", "VOID_TYPE"}:
                items.append(self.parse_function_declaration())
            else:
                items.append(self.parse_statement())
        return Program(items)

    def parse_function_declaration(self):
        return_type = self.tokenizer.next.type.replace("_TYPE", "").lower()
        self.tokenizer.select_next()
        if self.tokenizer.next.type != "FUNCTION":
            raise Exception("Expected 'function'")
        self.tokenizer.select_next()
        if self.tokenizer.next.type != "IDENTIFIER":
            raise Exception("Expected function name")
        name = self.tokenizer.next.value
        self.tokenizer.select_next()
        args = self.parse_parameter_list()
        body = self.parse_block()
        return FuncDecl(return_type, name, args, body)

    def parse_parameter_list(self):
        params = []
        if self.tokenizer.next.type != "LPAREN":
            raise Exception("Expected '(' after function name")
        self.tokenizer.select_next()
        if self.tokenizer.next.type != "RPAREN":
            param_type = self.tokenizer.next.type.replace("_TYPE", "").lower()
            self.tokenizer.select_next()
            if self.tokenizer.next.type != "IDENTIFIER":
                raise Exception("Expected parameter name")
            name = self.tokenizer.next.value
            self.tokenizer.select_next()
            params.append((param_type, name))
            while self.tokenizer.next.type == "COMMA":
                self.tokenizer.select_next()
                param_type = self.tokenizer.next.type.replace("_TYPE", "").lower()
                self.tokenizer.select_next()
                if self.tokenizer.next.type != "IDENTIFIER":
                    raise Exception("Expected parameter name")
                name = self.tokenizer.next.value
                self.tokenizer.select_next()
                params.append((param_type, name))
        if self.tokenizer.next.type != "RPAREN":
            raise Exception("Expected ')' after parameter list")
        self.tokenizer.select_next()
        return params

    def parse_block(self):
        if self.tokenizer.next.type != "LBRACE":
            raise Exception("Expected '{'")
        self.tokenizer.select_next()
        stmts = []
        while self.tokenizer.next.type != "RBRACE":
            stmts.append(self.parse_statement())
        self.tokenizer.select_next()
        return Block(stmts)

    def parse_statement(self):
        if self.tokenizer.next.type == "LET":
            return self.parse_variable_declaration()
        elif self.tokenizer.next.type == "IF":
            return self.parse_if()
        elif self.tokenizer.next.type == "FOR":
            return self.parse_for()
        elif self.tokenizer.next.type == "WHILE":
            return self.parse_while()
        elif self.tokenizer.next.type == "ECHO_KW":
            return self.parse_echo()
        elif self.tokenizer.next.type == "RETURN":
            return self.parse_return()
        elif self.tokenizer.next.type == "BANG_LINE":
            content = self.tokenizer.next.value
            self.tokenizer.select_next()
            if self.tokenizer.next.type != "SEMI":
                raise Exception("Expected ';'")
            self.tokenizer.select_next()
            return InlineCommand(content)
        elif self.tokenizer.next.type == "IDENTIFIER":
            name = self.tokenizer.next.value
            self.tokenizer.select_next()
            if self.tokenizer.next.type == "ASSIGN":
                self.tokenizer.select_next()
                value = self.parse_expression()
                if self.tokenizer.next.type != "SEMI":
                    raise Exception("Expected ';'")
                self.tokenizer.select_next()
                return Assignment(name, value)
            elif self.tokenizer.next.type == "LPAREN":
                args = self.parse_argument_list()
                if self.tokenizer.next.type != "SEMI":
                    raise Exception("Expected ';'")
                self.tokenizer.select_next()
                func_call = FuncCall(name, args)
                func_call.capture_output = False  # Direct call
                return func_call
        raise Exception("Invalid statement")

    def parse_variable_declaration(self):
        self.tokenizer.select_next()
        if self.tokenizer.next.type != "IDENTIFIER":
            raise Exception("Expected variable name")
        name = self.tokenizer.next.value
        self.tokenizer.select_next()
        if self.tokenizer.next.type != "COLON":
            raise Exception("Expected ':'")
        self.tokenizer.select_next()
        if not self.tokenizer.next.type.endswith("_TYPE"):
            raise Exception("Expected type after ':'")
        var_type = self.tokenizer.next.type.replace("_TYPE", "").lower()
        self.tokenizer.select_next()

        init_value = None
        if self.tokenizer.next.type == "ASSIGN":
            self.tokenizer.select_next()
            init_value = self.parse_expression()

        if self.tokenizer.next.type != "SEMI":
            raise Exception("Expected ';'")
        self.tokenizer.select_next()
        return VarDecl(var_type, name, init_value)

    def parse_if(self):
        self.tokenizer.select_next()
        if self.tokenizer.next.type != "LPAREN":
            raise Exception("Expected '(' after if")
        self.tokenizer.select_next()
        cond = self.parse_expression()
        if self.tokenizer.next.type != "RPAREN":
            raise Exception("Expected ')'")
        self.tokenizer.select_next()
        then_block = self.parse_block()
        else_block = None
        if self.tokenizer.next.type == "ELSE":
            self.tokenizer.select_next()
            else_block = self.parse_block()
        return If(cond, then_block, else_block)

    def parse_for(self):
        self.tokenizer.select_next()
        if self.tokenizer.next.type != "LPAREN":
            raise Exception("Expected '(' after for")
        self.tokenizer.select_next()
        if self.tokenizer.next.type != "IDENTIFIER":
            raise Exception("Expected identifier")
        var = self.tokenizer.next.value
        self.tokenizer.select_next()
        if self.tokenizer.next.type != "IN":
            raise Exception("Expected 'in'")
        self.tokenizer.select_next()
        start = self.parse_expression()
        if self.tokenizer.next.type != "DOTDOT":
            raise Exception("Expected '..'")
        self.tokenizer.select_next()
        end = self.parse_expression()
        if self.tokenizer.next.type != "RPAREN":
            raise Exception("Expected ')'")
        self.tokenizer.select_next()
        body = self.parse_block()
        return For(var, start, end, body)

    def parse_while(self):
        self.tokenizer.select_next()
        if self.tokenizer.next.type != "LPAREN":
            raise Exception("Expected '(' after while")
        self.tokenizer.select_next()
        cond = self.parse_expression()
        if self.tokenizer.next.type != "RPAREN":
            raise Exception("Expected ')'")
        self.tokenizer.select_next()
        return While(cond, self.parse_block())

    def parse_echo(self):
        self.tokenizer.select_next()
        if self.tokenizer.next.type != "LPAREN":
            raise Exception("Expected '('")
        self.tokenizer.select_next()
        expr = self.parse_expression()
        if self.tokenizer.next.type != "RPAREN":
            raise Exception("Expected ')'")
        self.tokenizer.select_next()
        if self.tokenizer.next.type != "SEMI":
            raise Exception("Expected ';'")
        self.tokenizer.select_next()
        return Echo(expr)

    def parse_return(self):
        self.tokenizer.select_next()
        if self.tokenizer.next.type == "SEMI":
            self.tokenizer.select_next()
            return Return(None)
        expr = self.parse_expression()
        if self.tokenizer.next.type != "SEMI":
            raise Exception("Expected ';'")
        self.tokenizer.select_next()
        return Return(expr)

    def parse_expression(self):
        return self.parse_b_expression()

    def parse_b_expression(self):
        left = self.parse_b_term()
        while self.tokenizer.next.type == "OR":
            op = self.tokenizer.next.type
            self.tokenizer.select_next()
            right = self.parse_b_term()
            left = BinOp(op, left, right)
        return left

    def parse_b_term(self):
        left = self.parse_rel_expression()
        while self.tokenizer.next.type == "AND":
            op = self.tokenizer.next.type
            self.tokenizer.select_next()
            right = self.parse_rel_expression()
            left = BinOp(op, left, right)
        return left

    def parse_rel_expression(self):
        left = self.parse_simple_expression()
        if self.tokenizer.next.type in {"EQ", "NEQ", "GT", "LT", "GTE", "LTE"}:
            op = self.tokenizer.next.type
            self.tokenizer.select_next()
            right = self.parse_simple_expression()
            return BinOp(op, left, right)
        return left

    def parse_simple_expression(self):
        left = self.parse_term()
        while self.tokenizer.next.type in {"PLUS", "MINUS"}:
            op = self.tokenizer.next.type
            self.tokenizer.select_next()
            right = self.parse_term()
            left = BinOp(op, left, right)
        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.tokenizer.next.type in {"MUL", "DIV", "MOD"}:
            op = self.tokenizer.next.type
            self.tokenizer.select_next()
            right = self.parse_factor()
            left = BinOp(op, left, right)
        return left

    def parse_factor(self):
        token = self.tokenizer.next
        if token.type == "INT":
            self.tokenizer.select_next()
            return IntVal(token.value)
        elif token.type == "STRING":
            self.tokenizer.select_next()
            return StringVal(token.value)
        elif token.type == "BOOL":
            self.tokenizer.select_next()
            return BoolVal(token.value)
        elif token.type == "IDENTIFIER":
            name = token.value
            self.tokenizer.select_next()
            if self.tokenizer.next.type == "LPAREN":
                args = self.parse_argument_list()
                return FuncCall(name, args)
            return Identifier(name)
        elif token.type == "READ":
            self.tokenizer.select_next()
            if self.tokenizer.next.type != "LPAREN":
                raise Exception("Expected '(' after read")
            self.tokenizer.select_next()
            # Allow empty argument list for read()
            if self.tokenizer.next.type == "RPAREN":
                self.tokenizer.select_next()
                return Read()
            else:
                # Parse the prompt argument if provided
                prompt = self.parse_expression()
                if self.tokenizer.next.type != "RPAREN":
                    raise Exception("Expected ')' after read argument")
                self.tokenizer.select_next()
                return Read(prompt)
        elif token.type == "BANG_EXPR":
            self.tokenizer.select_next()
            return CaptureCommand(token.value)
        elif token.type in {"PLUS", "MINUS", "NOT"}:
            op = token.type
            self.tokenizer.select_next()
            return UnOp(op, self.parse_factor())
        elif token.type == "LPAREN":
            self.tokenizer.select_next()
            expr = self.parse_expression()
            if self.tokenizer.next.type != "RPAREN":
                raise Exception("Expected ')'")
            self.tokenizer.select_next()
            return expr
        else:
            raise Exception(f"Unexpected token in expression: {token.type}")
        
    def parse_argument_list(self):
        args = []
        if self.tokenizer.next.type != "LPAREN":
            raise Exception("Expected '('")
        self.tokenizer.select_next()
        if self.tokenizer.next.type != "RPAREN":
            args.append(self.parse_expression())
            while self.tokenizer.next.type == "COMMA":
                self.tokenizer.select_next()
                args.append(self.parse_expression())
        if self.tokenizer.next.type != "RPAREN":
            raise Exception("Expected ')'")
        self.tokenizer.select_next()
        return args