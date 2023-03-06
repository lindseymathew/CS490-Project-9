from filecrawler import crawlDirectory
from parser import generateFileASTs

import ast

def createIgnoreList():
  with open('.ignore') as f:
    return f.read().splitlines()

def main():
  print('Python Program Analysis Tool')
  print('Please input the Python project relative or absolute path.')
  projectPath = input('Path: ')

  filePaths = crawlDirectory(projectPath, createIgnoreList())
  fileASTs = generateFileASTs(filePaths)

  for file in fileASTs:
    for node in ast.walk(file):
      print(f'Nodetype: {type(node).__name__:{16}} {node}')

main()