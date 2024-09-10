import ast
import random
import string
import sys

class Obfuscator(ast.NodeTransformer):
    def __init__(self):
        self.function_names = {}
        self.variable_names = {}
        self.string_literals = {}

    def visit_FunctionDef(self, node):
        # Rename function
        new_name = self.generate_random_name()
        self.function_names[node.name] = new_name
        node.name = new_name

        # Reorder code blocks
        random.shuffle(node.body)

        # Insert dead code
        node.body.insert(0, ast.Pass())

        return self.generic_visit(node)

    def visit_Name(self, node):
        # Rename variable
        if node.id in self.variable_names:
            node.id = self.variable_names[node.id]
        else:
            new_name = self.generate_random_name()
            self.variable_names[node.id] = new_name
            node.id = new_name

        return node

    def visit_If(self, node):
        # Obfuscate conditional statement
        node.test = self.obfuscate_conditional(node.test)

        return self.generic_visit(node)

    def visit_For(self, node):
        # Obfuscate loop
        node.iter = self.obfuscate_loop(node.iter)

        return self.generic_visit(node)

    def visit_Str(self, node):
        # Encrypt string literal
        encrypted_str = self.encrypt_string(node.s)
        node.s = encrypted_str

        return node

    def generate_random_name(self):
        return ''.join(random.choice(string.ascii_letters + string.digits + '_') for _ in range(10))

    def obfuscate_conditional(self, node):
        # Replace conditional statement with an equivalent but more complex expression
        if isinstance(node, ast.NameConstant):
            return ast.UnaryOp(ast.Not(), node)
        elif isinstance(node, ast.UnaryOp):
            return ast.NameConstant(not node.operand.n)
        else:
            return node

    def obfuscate_loop(self, node):
        # Replace loop with a recursive function
        func_name = self.generate_random_name()
        self.function_names[func_name] = func_name

        def recursive_func(iterable, func):
            if iterable:
                func(iterable[0])
                recursive_func(iterable[1:], func)

        return ast.Call(ast.Name(func_name, ast.Load()), [node], [])

    def encrypt_string(self, s):
        encrypted_str = ''
        for c in s:
            encrypted_str += chr(ord(c) + 3)  # Simple substitution cipher
        return encrypted_str

def obfuscate_code(code):
    tree = ast.parse(code)
    obfuscator = Obfuscator()
    obfuscated_tree = obfuscator.visit(tree)
    return ast.unparse(obfuscated_tree)

def main():
    print("Enter multi-line code (enter 'done' to finish):")
    code = []
    while True:
        line = input()
        if line.strip() == 'done':
            break
        code.append(line)
    code = '\n'.join(code)

    obfuscated_code = obfuscate_code(code)
    print("Obfuscated code:")
    print(obfuscated_code)

if __name__ == '__main__':
    main()