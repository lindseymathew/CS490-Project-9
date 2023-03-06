import ast

def generateProgramAST(program):
  return ast.parse(program)

def generateFileASTs(filePaths):
  content = []
  for path in filePaths:
    with open(path, 'r') as f:
      content.append(generateProgramAST(f.read()))
  return content
