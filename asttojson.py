import ast
import acceptedattr

# Note: modified version of https://pypi.org/project/ast2json/

BUILTIN_PURE = (int, float, bool)
BUILTIN_BYTES = (bytearray, bytes)
BUILTIN_STR = (str)

def decode_str(value):
  return value

def decode_bytes(value):
  try:
    return value.decode('utf-8')
  except:
    return codecs.getencoder('hex_codec')(value)[0].decode('utf-8')

 # Modified addition of ast2json where unnecessary attributes are filtered out.
def accepted_attr(node, attr):
  try:
    return attr in acceptedattr.create_accepted_attr()[type(node)]
  except:
    print('Note: ' + str(type(node)) + ' not included in attribute dictionary.')
    return True

def ast2json(node):
  assert isinstance(node, ast.AST)
  to_return = dict()
  to_return['_type'] = node.__class__.__name__
  for attr in dir(node):
    if attr.startswith("_") or not accepted_attr(node, attr):
      continue
    to_return[attr] = get_value(getattr(node, attr))
  return to_return


def str2json(string):
  return ast2json(ast.parse(string))


def get_value(attr_value):
  if attr_value is None:
    return attr_value
  if isinstance(attr_value, BUILTIN_PURE):
    return attr_value
  if isinstance(attr_value, BUILTIN_BYTES):
    return decode_bytes(attr_value)
  if isinstance(attr_value, BUILTIN_STR):
    return decode_str(attr_value)
  if isinstance(attr_value, complex):
    return str(attr_value)
  if isinstance(attr_value, list):
    return [get_value(x) for x in attr_value]
  if isinstance(attr_value, ast.AST):
    return ast2json(attr_value)
  if isinstance(attr_value, type(Ellipsis)):
    return '...'
  else:
    raise Exception("unknown case for '%s' of type '%s'" % (attr_value, type(attr_value)))


"""
We are only interested in Import, ImportFrom, and Call nodes.
This function filters out those nodes and creates JSON data for those nodes
specifically.
"""
def convert_ast_to_json(root):
  result = []
  for node in ast.walk(root):
    if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom) or isinstance(node, ast.Call):
      result.append(ast2json(node))

  return result
  
