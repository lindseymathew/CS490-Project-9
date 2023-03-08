import ast

def generate_program_ast(program):
  return ast.parse(program)

def generate_file_ast(file_paths):
  content = []
  for path in file_paths:
    with open(path, 'r') as f:
      try:
        content.append(generate_program_ast(f.read()))
      except Exception as e:
        print('ERROR: cannot read file', path)
        print('Exception:', e, '\n')
  return content
