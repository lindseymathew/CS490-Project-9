from collections import deque
import ast

class AstConverter:
  '''General purpose class for converting a abstract syntax tree (AST) generated
  by the Python ast module
  '''

  def __init__(self):
    # Used for substitutions when aliases are encountered in the conversion
    # process.
    self.aliases = {}

  def run(self, root):
    '''We are only interested in Import, ImportFrom, Call, and FunctionDef nodes.
    
    This function returns a simplified JSON representation of an AST,
    segregated by Import, ImportFrom, Call, and FunctionDef nodes.
    '''

    return self.walk_ast(root)

  def get_function_names(self, root):
    '''Returns all the function names of a node as a list.

    Example:

    return_test().walk().hello_world()

    yields

    ['return_test', 'walk', 'hello_world']
    '''
    if isinstance(root, ast.Name):
      if root.id in self.aliases:
        return [self.aliases[root.id]]
      return [root.id]
    elif isinstance(root, ast.Attribute):
      return self.get_function_names(root.value) + [root.attr]
    elif isinstance(root, ast.Call):
      return self.get_function_names(root.func)
    else:
      key = ast.unparse(root)
      if key in self.aliases:
        return [self.aliases[key]]
      return [key]

  def convert_call(self, root):
    '''Converts Call nodes into a dictionary with the fields 'function', args',
    and 'keywords'.

    Example:
    hello_world(test = 3, 7)

    yields

    {
      'function': 'hello_world',
      'args': [
        '7'
      ],
      'keywords': [
        {
          'keyword': 'test',
          'value': '3'
        }
      ]
    }

    '''
    call = {}
    call['function'] = self.get_function_names(root.func)

    args = []
    for node in root.args:
      if isinstance(node, ast.Call):
        args.append(self.convert_call(node))
      else:
        args.append(ast.unparse(node))
    
    keywords = []
    for node in root.keywords:
      keyword = {}
      keyword['keyword'] = node.arg
      keyword['value'] = ast.unparse(node.value)
      keywords.append(keyword)

    call['args'] = args
    call['keywords'] = keywords
    return call

  def convert_import(self, root):
    '''Converts Import nodes into a dictionary with a 'names' field containing
    a list of import aliases.

    Example:

    import ast as a
    
    yields

    {
      'names': {
        {
          'name': 'ast',
          'alias': 'a'
        }
      }
    }
    '''
    import_res = {}
    import_aliases = []
    for z in root.names:
      alias = {}
      alias['name'] = z.name
      alias['alias'] = z.asname
      if z.asname != None:
        self.aliases[z.asname] = z.name
      import_aliases.append(alias)
    import_res['names'] = import_aliases
    return import_res

  def convert_import_from(self, root):
    '''Converts ImportFrom nodes into a dictionary with 'module' and 'names'
    fields.

    Example:

    from ast import parse as p
    
    yields

    {
      'module': 'ast'
      'names': {
        {
          'name': 'parse',
          'alias': 'p'
        }
      }
    }
    '''
    import_from = {}
    import_from['module'] = root.module
    import_aliases = []
    for z in root.names:
      alias = {}
      alias['name'] = z.name
      alias['alias'] = z.asname
      if z.asname != None:
        self.aliases[z.asname] = z.name
      import_aliases.append(alias)
    import_from['names'] = import_aliases
    return import_from

  def convert_function_defs(self, root):
    '''Converts Function nodes into a dictionary with the fields 'names',
    'args', 'calls', and 'function_defs'.

    'calls' and 'function_defs' are used to represent calls and function
    definitions, respectively, that are nested within the body of the
    function definition.

    Example:
    def hello_world(test = 3):
      print()
      print_out()

      def test_1():
        return None

    yields

    {
      'name': 'hello_world',
      'args': [
        'test'
      ],
      'calls': [
        {
          "function": [
            "print"
          ],
          "args": [],
          "keywords": []
        },
        {
          "function": [
            "print_out"
          ],
          "args": [],
          "keywords": []
        }
      ],
      'function_defs': [
        {
          "name": "test_1",
          "args": [],
          "calls": [],
          "function_defs": []
        }
      ]
    }

    '''
    function = {}
    function['name'] = root.name
    function['args'] = [ast.unparse(arg) for arg in root.args.args]
    
    calls = []
    function_defs = []
    for item in root.body:
      nested_values = self.walk_function_def((item))
      calls = calls + nested_values['calls']
      function_defs = function_defs + nested_values['function_defs']
    
    function['calls'] = calls
    function['function_defs'] = function_defs
    return function

  def walk_function_def(self, root):
    '''Traverses FunctionDef nodes to find nested call and function definition
    nodes.
    
    This function traverses (in BFS fashion) function definitions and
    returns a dictionary containing 'call' and 'function_defs' fields.
    This is used to find nested Call and FunctionDef nodes in the original
    FunctionDef node.
    '''

    res = {}
    res['calls'] = []
    res['function_defs'] = []

    todo = deque([root])
    while todo:
      node = todo.popleft()

      if isinstance(node, ast.Call):
        res['calls'].append(self.convert_call(node))
      elif isinstance(node, ast.FunctionDef):
        res['function_defs'].append(self.convert_function_defs(node))
      else:
        # If-statement guarantees a single visit for Call/FunctionDef
        # nodes.
        todo.extend(ast.iter_child_nodes(node))
    return res


  def walk_ast(self, node):
    '''Traverses AST to find Import, ImportFrom, Call, and FunctionDef nodes.
    
    This function traverses (in BFS fashion) the AST and returns a dictionary
    containing 'imports', 'import_froms', 'call', and 'function_defs' fields.
    
    We are mainly interested in Import, ImportFrom, Call, and FunctionDef
    nodes.
    '''

    res = {}

    res['imports'] = []
    res['import_froms'] = []
    res['calls'] = []
    res['function_defs'] = []

    todo = deque([node])
    while todo:
      node = todo.popleft()

      if isinstance(node, ast.Import):
        res['imports'].append(self.convert_import(node))
      elif isinstance(node, ast.ImportFrom):
        res['import_froms'].append(self.convert_import_from(node))
      elif isinstance(node, ast.Call):
        res['calls'].append(self.convert_call(node))
      elif isinstance(node, ast.FunctionDef):
        res['function_defs'].append(self.convert_function_defs(node))
      else:
        # If-statement guarantees a single visit for Call/FunctionDef
        # nodes.
        todo.extend(ast.iter_child_nodes(node))

    return res
