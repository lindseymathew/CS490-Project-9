import ast

"""Creates a dictionary of attributes that are keyed by class name

ASTs include a lot of information that we are not specifically interested in.
In order to filter out those attributes, this function will return a dict
that contains all the accepted attributes by class name. Using this,
unecessary attributes are filtered out.
"""
def create_accepted_attr():
  attrdict = {}
  attrdict[ast.Import] = ['names']
  attrdict[ast.alias] = ['name', 'asname']
  attrdict[ast.ImportFrom] = ['module', 'names']

  attrdict[ast.BoolOp] = ['op', 'values']
  attrdict[ast.BinOp] = ['left', 'right', 'op']
  attrdict[ast.UnaryOp] = ['op', 'operand']
  attrdict[ast.UnaryOp] = ['op', 'operand']
  attrdict[ast.Lambda] = ['args', 'body']
  attrdict[ast.IfExp] = ['test', 'body', 'orelse']
  attrdict[ast.Dict] = ['keys', 'values']
  attrdict[ast.Set] = ['elts']
  attrdict[ast.ListComp] = ['elt', 'generators']
  attrdict[ast.SetComp] = ['elt', 'generators']
  attrdict[ast.DictComp] = ['key', 'value', 'generators']
  attrdict[ast.GeneratorExp] = ['elt', 'generators']

  attrdict[ast.Await] = ['value']
  attrdict[ast.Yield] = ['value']
  attrdict[ast.YieldFrom] = ['value']

  attrdict[ast.Compare] = ['left', 'ops', 'comparators']
  attrdict[ast.Call] = ['func', 'keywords', 'args']
  attrdict[ast.FormattedValue] = ['value', 'conversion', 'format_spec']
  attrdict[ast.JoinedStr] = ['values']
  attrdict[ast.Constant] = ['value', 'kind']

  attrdict[ast.Attribute] = ['attr', 'value']
  attrdict[ast.Subscript] = ['value', 'slice']
  attrdict[ast.Starred] = ['value']
  attrdict[ast.Name] = ['id']
  attrdict[ast.List] = ['elts']
  attrdict[ast.Tuple] = ['elts']

  attrdict[ast.Slice] = ['lower', 'upper', 'step']

  attrdict[ast.comprehension] = ['target', 'iter', 'ifs', 'is_async']

  attrdict[ast.arg] = ['arg', 'annotation']
  attrdict[ast.keyword] = ['arg', 'value']

  attrdict[ast.withitem] = ['context_expr']
  attrdict[ast.Index] = ['value']

  attrdict[ast.Str] = ['s']
  attrdict[ast.Num] = ['n']
  attrdict[ast.Bytes] = ['s']

  return attrdict
