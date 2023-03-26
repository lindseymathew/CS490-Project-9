from collections import deque
import ast

def get_function_names(root):
  if isinstance(root, ast.Name):
    return [root.id]
  elif isinstance(root, ast.Attribute):
    print(ast.dump(root))
    return get_function_names(root.value) + [root.attr]
  elif isinstance(root, ast.Call):
    return get_function_names(root.func)
  else:
    return [ast.unparse(root)]

def convert_call(root):
  call = {}
  call['function'] = get_function_names(root.func)

  args = []
  for node in root.args:
    if isinstance(node, ast.Call):
      args.append(convert_call(node))
    else:
      args.append(ast.unparse(node))
  
  keywords = []
  for node in root.keywords:
    keyword = {}
    keyword['var'] = node.arg
    keyword['value'] = ast.unparse(node.value)
    keywords.append(keyword)

  call['args'] = args
  call['keywords'] = keywords
  return call

def convert_import(root):
  import_res = {}
  aliases = []
  for z in root.names:
    alias = {}
    alias['name'] = z.name
    alias['alias'] = z.asname
    aliases.append(alias)
  import_res['names'] = aliases
  return import_res

def convert_import_from(root):
  import_from = {}
  import_from['module'] = root.module
  aliases = []
  for z in root.names:
    alias = {}
    alias['name'] = z.name
    alias['alias'] = z.asname
    aliases.append(alias)
  import_from['names'] = aliases
  return import_from

def convert_function_defs(root):
  function = {}
  function['name'] = root.name
  function['args'] = [ast.unparse(arg) for arg in root.args.args]
  
  calls = []
  function_defs = []
  for item in root.body:
    nested_values = walk_function_def((item))
    calls = calls + nested_values['calls']
    function_defs = function_defs + nested_values['function_defs']
  
  function['calls'] = calls
  function['function_defs'] = function_defs
  return function

def walk_function_def(root):
  res = {}
  res['calls'] = []
  res['function_defs'] = []

  todo = deque([root])
  while todo:
    add_children = True
    node = todo.popleft()

    if isinstance(node, ast.Call):
      res['calls'].append(convert_call(node))
      add_children = False
    
    if isinstance(node, ast.FunctionDef):
      res['function_defs'].append(convert_function_defs(node))
      add_children = False

    if add_children:
      todo.extend(ast.iter_child_nodes(node))
  return res


def walk_ast(node):
  res = {}

  res['imports'] = []
  res['import_froms'] = []
  res['calls'] = []
  res['function_defs'] = []

  todo = deque([node])
  while todo:
    add_children = True
    node = todo.popleft()

    if isinstance(node, ast.Call):
      res['calls'].append(convert_call(node))
      add_children = False
    
    if isinstance(node, ast.Import):
      res['imports'].append(convert_import(node))
      add_children = False
    
    if isinstance(node, ast.ImportFrom):
      res['import_froms'].append(convert_import_from(node))
      add_children = False
    
    if isinstance(node, ast.FunctionDef):
      res['function_defs'].append(convert_function_defs(node))
      add_children = False

    if add_children:
      todo.extend(ast.iter_child_nodes(node))

  return res
        


'''
We are only interested in Import, ImportFrom, Call, and FunctionDef nodes.
This function filters out those nodes and creates JSON data for those nodes
specifically.
'''
def convert_ast_to_json(root):

  return walk_ast(root)

