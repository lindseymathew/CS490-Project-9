import ast

def generateProgramAST(program):
  return ast.parse(program)

def generateFileASTs(filePaths):
  content = []
  for path in filePaths:
    with open(path, 'r') as f:
      try:
        content.append(generateProgramAST(f.read()))
      except Exception as e:
        print('ERROR: cannot read file', path)
        print('Exception:', e, '\n')
  return content
