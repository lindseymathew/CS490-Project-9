import ast

def readFiles(filePaths):
  content = []
  for path in filePaths:
    with open(path, 'r') as f:
      content.append(f.read())
  
  return content

def parseProgram(program):
  return ast.parse(program, mode='eval')
