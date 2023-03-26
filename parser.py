import ast

def generate_source_ast(source):
  return ast.parse(source)

"""
Generates an AST for each file specified in file_paths.
"""
def generate_file_ast(file_paths):
  content = []
  for path in file_paths:
    with open(path, 'r') as f:
      try:
        content.append([path, generate_source_ast(f.read())])
      except Exception as e:
        print('ERROR: cannot read file', path)
        print('Exception:', e, '\n')
  return content
