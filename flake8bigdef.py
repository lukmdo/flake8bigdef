try:
    import ast
    from ast import iter_child_nodes
except ImportError:
    # fallback for python2.5 and older
    from flake8.util import ast, iter_child_nodes


NAME = 'flake8-bigdef'
VERSION = (0, 0, 1)
__version__ = VERSION
__versionstr__ = '.'.join(map(str, VERSION))


class Checker(object):
    name = NAME
    version = __versionstr__
    MAX_LEN = 5
    code = 'e501'
    message = '{code} Function {name} too long ({got} > {max} lines)'

    def __init__(self, tree, filename=None):
        self.tree = tree
        self.filename = filename

    def format_message(self, name, length):
        return self.message.format(
            code=self.code, name=name, got=length, max=self.MAX_LEN)

    def check_node(self, node):
        todo = []
        name_prefix = ''
        if isinstance(node, ast.FunctionDef):
            todo = (node,)
        elif isinstance(node, ast.ClassDef):
            name_prefix = node.name + '.'
            todo = (
                n for n in iter_child_nodes(node) if isinstance(
                n, ast.FunctionDef))

        for node in todo:
            begin = node.lineno
            end = node.body[-1].lineno
            if len(node.body) > 1 and isinstance(node.body[0], ast.Expr):
                begin = node.body[0].lineno

            got_len = end - begin
            if got_len > self.MAX_LEN:
                yield (
                    node.lineno,
                    node.col_offset,
                    self.format_message(name_prefix + node.name, got_len),
                    Checker)

    def run(self):
        for node in iter_child_nodes(self.tree):
            for error in self.check_node(node):
                yield error
