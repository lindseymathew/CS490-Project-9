import ast

def generate_program_AST(program):
  return ast.parse(program)

def generate_file_AST(filePaths):
  content = []
  for path in filePaths:
    with open(path, 'r') as f:
      try:
        content.append(generate_program_AST(f.read()))
      except Exception as e:
        print('ERROR: cannot read file', path)
        print('Exception:', e, '\n')
  return content
