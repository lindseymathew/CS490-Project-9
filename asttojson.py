import ast
from ast2json import ast2json

def convert_ast_to_json(root):
  result = []
  for node in ast.walk(root):
    if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom) or isinstance(node, ast.Call):
      result.append(ast2json(node))

  return result
  
