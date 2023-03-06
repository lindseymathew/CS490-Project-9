from crawler import crawlDirectory
from parser import readFiles

def createIgnoreList():
  with open('./.ignore') as f:
    return f.read().splitlines()

def main():
  print('Python Program Analysis Tool')
  print('Please input the Python project relative or absolute path.')
  projectPath = input('Path: ')

  filePaths = crawlDirectory(projectPath, createIgnoreList())
  fileContents = readFiles(filePaths)
  print(fileContents)

main()