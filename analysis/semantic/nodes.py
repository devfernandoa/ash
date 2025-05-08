def inject_param_map(node, param_map):
    if isinstance(node, Node):
        # Set param_map on all nodes, not just Identifiers
        node.param_map = param_map
        
        # For all other node types, recursively process children
        for field_name in vars(node):
            field_value = getattr(node, field_name)
            if isinstance(field_value, Node):
                inject_param_map(field_value, param_map)
            elif isinstance(field_value, list):
                for item in field_value:
                    if isinstance(item, Node):
                        inject_param_map(item, param_map)

class Node:
    def __init__(self, *children):
        self.children = list(children)

    def generate(self):
        raise NotImplementedError("Each node must implement its own generate method.")


class Program(Node):
    def __init__(self, statements):
        super().__init__(*statements)

    def generate(self):
        return "\n".join(child.generate() for child in self.children)


class VarDecl(Node):
    def __init__(self, var_type, name, value=None):
        self.var_type = var_type
        self.name = name
        self.value = value

    def generate(self):
        if self.value:
            if isinstance(self.value, Read):
            # Special case for read commands - don't use = sign
                return f"{self.value.generate()} {self.name}"
            return f"{self.name}={self.value.generate()}"
        return f"# declared {self.var_type} {self.name}"


class Assignment(Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def generate(self):
        if isinstance(self.value, Read):
            return f"{self.value.generate()} {self.name}"
        
        if isinstance(self.value, BinOp) and self.value.op == "MOD":
            left = self.value.children[0].generate()
            right = self.value.children[1].generate()
            return f"{self.name}=$(( {left} % {right} ))"
        
        if isinstance(self.value, BinOp) and self.value.op == "PLUS":
            left = self.value.children[0].generate()
            right = self.value.children[1].generate()
            return f"{self.name}=$(( {left} + {right} ))"
        
        # Make sure we handle variable references on the right side properly
        if isinstance(self.value, Identifier):
            return f"{self.name}={self.value.generate()}"
        
        return f"{self.name}={self.value.generate()}"

class FuncCall(Node):
    def __init__(self, name, args):
        self.name = name
        self.args = args
        self.capture_output = True  # Always capture output for function calls in expressions

    def generate(self):
        args_str = " ".join(arg.generate() for arg in self.args)
        if self.capture_output:
            return f'$( {self.name} {args_str} )'
        return f'{self.name} {args_str}'

class Echo(Node):
    def __init__(self, expr):
        self.expr = expr

    def generate(self):
        if isinstance(self.expr, BinOp) and self.expr.op == "PLUS":
            # Handle string concatenation directly in echo
            left = self.expr.children[0].generate().strip('"')
            right = self.expr.children[1].generate().strip('"')
            return f'echo "{left}{right}"'
        # Make sure we properly generate variable references in echo statements
        return f'echo {self.expr.generate()}'


class Return(Node):
    def __init__(self, expr):
        self.expr = expr

    def generate(self):
        if self.expr is None:
            return "return"
        
        # Handle boolean results
        if isinstance(self.expr, BinOp) and self.expr.op in ["EQ", "NEQ", "GT", "LT", "GTE", "LTE"]:
            return f'if (( {self.expr.generate()} )); then echo true; else echo false; fi\nreturn'
        
        return f"echo {self.expr.generate()}\nreturn"


class InlineCommand(Node):
    def __init__(self, command):
        self.command = command

    def generate(self):
        return self.command


class CaptureCommand(Node):
    def __init__(self, command):
        self.command = command

    def generate(self):
        return f'$( {self.command} )'


class IntVal(Node):
    def __init__(self, value):
        self.value = value

    def generate(self):
        return str(self.value)


class StringVal(Node):
    def __init__(self, value):
        self.value = value

    def generate(self):
        return f'\"{self.value}\"'


class BoolVal(Node):
    def __init__(self, value):
        self.value = value
        self.is_conditional = False

    def generate(self):
        if self.is_conditional:
            return "1" if self.value else "0"
        return "true" if self.value else "false"


class Identifier(Node):
    def __init__(self, name):
        self.name = name

    def generate(self):
        # For parameters in functions (handled via param_map), use raw name
        if hasattr(self, "param_map") and self.name in self.param_map:
            return f"${self.name}"  # Always add $ for variables
        # For all other cases, add $ prefix
        return f"${self.name}"

class Read(Node):
    def __init__(self, prompt=None):
        self.prompt = prompt

    def generate(self):
        if self.prompt:
            return f'read -p "{self.prompt.generate()}"'
        return 'read'

class BinOp(Node):
    def __init__(self, op, left, right):
        self.op = op
        super().__init__(left, right)
        self.is_conditional = False  # Default to arithmetic context

    def generate(self):
        op_map = {
            "PLUS": "+",
            "MINUS": "-",
            "MUL": "*",
            "DIV": "/",
            "MOD": "%",
            "EQ": "==",
            "NEQ": "!=",
            "GT": ">",
            "LT": "<",
            "GTE": ">=",
            "LTE": "<=",
            "AND": "&&",
            "OR": "||"
        }
        
        if self.op not in op_map:
            raise Exception(f"Unknown binary operator: {self.op}")
            
        bash_op = op_map[self.op]
        left = self.children[0].generate()
        right = self.children[1].generate()

        # Handle string concatenation
        if self.op == "PLUS":
            if isinstance(self.children[0], (StringVal, Identifier)) and \
               isinstance(self.children[1], (StringVal, Identifier)) and \
               not self.is_conditional:
                print(f"String concatenation detected: {left} + {right}")
                left = left.strip('"')
                right = right.strip('"')
                return f'"{left}{right}"'
        
        # Handle conditional context (if/while conditions)
        if self.is_conditional:
            return f"(( {left} {bash_op} {right} ))"
        
        # Handle arithmetic operations
        if self.op in ["PLUS", "MINUS", "MUL", "DIV", "MOD"]:
            return f"$(( {left} {bash_op} {right} ))"
        
        # Handle boolean comparisons in arithmetic context
        if self.op in ["EQ", "NEQ", "GT", "LT", "GTE", "LTE"]:
            return f"$(( {left} {bash_op} {right} ))"
        
        
        # Handle logical operators in non-conditional context
        return f"[ {left} {bash_op} {right} ]"

class UnOp(Node):
    def __init__(self, op, expr):
        self.op = op
        super().__init__(expr)

    def generate(self):
        value = self.children[0].generate()
        if self.op == "+":
            return f"$(({value}))"
        elif self.op == "-":
            return f"$((-{value}))"
        elif self.op == "!":
            return f"! {value}"
        else:
            raise Exception(f"Unknown unary operator {self.op}")

class Block(Node):
    def __init__(self, statements):
        super().__init__(*statements)

    def generate(self):
        return "\n".join(stmt.generate() for stmt in self.children)


class FuncDecl(Node):
    def __init__(self, return_type, name, params, body):
        self.return_type = return_type
        self.name = name
        self.params = params
        self.body = body

    def generate(self):
        # Create parameter initialization and mapping
        param_inits = []
        param_map = {}
        for i, (_, name) in enumerate(self.params):
            param_inits.append(f"local {name}=${i+1}")
            param_map[name] = name  # Reference local vars directly
            
        inject_param_map(self.body, param_map)
        
        body_code = self.body.generate()
        return f"{self.name}() {{\n{' ; '.join(param_inits)}\n{body_code}\n}}"

class If(Node):
    def __init__(self, condition, then_block, else_block=None):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block
        
        # Validate blocks aren't empty
        if not self.then_block.children:
            raise Exception("Empty 'then' block in if statement")
        if self.else_block and not self.else_block.children:
            raise Exception("Empty 'else' block in if statement")
            
        # Mark condition as being in conditional context
        if isinstance(self.condition, BinOp):
            self.condition.is_conditional = True

    def generate(self):
        cond_code = self.condition.generate()
        then_code = self.then_block.generate()
        if self.else_block:
            else_code = self.else_block.generate()
            return f"if {cond_code}; then\n{then_code}\nelse\n{else_code}\nfi"
        return f"if {cond_code}; then\n{then_code}\nfi"

class While(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
        
        # Validate block isn't empty
        if not self.body.children:
            raise Exception("Empty body in while loop")
            
        # Mark condition as being in conditional context
        if isinstance(self.condition, BinOp):
            self.condition.is_conditional = True

    def generate(self):
        return f"while {self.condition.generate()}; do\n{self.body.generate()}\ndone"
    
class For(Node):
    def __init__(self, var, start, end, body):
        self.var = var
        self.start = start
        self.end = end
        self.body = body

    def generate(self):
        return f"for {self.var} in $(seq {self.start.generate()} {self.end.generate()}); do\n{self.body.generate()}\ndone"