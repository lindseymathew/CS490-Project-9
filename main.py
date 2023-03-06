#!/usr/bin/env python3

from filecrawler import crawlDirectory
from parser import generateFileASTs

import ast
import sys
import os

def createIgnoreList():
  try:
    with open('.ignore') as f:
      return f.read().splitlines()
  except:
    f = open('.ignore', 'w')
    f.write('.ignore')
    f.close()
    return ['.ignore']

def main():
  if len(sys.argv) < 2:
    print('Python project path not found!\nUsage: ./main.py <relative/absolute project path>')
    return
  
  projectPath = sys.argv[1]
  print('Path entered:', os.path.abspath(projectPath))

  filePaths = crawlDirectory(projectPath, createIgnoreList())
  fileASTs = generateFileASTs(filePaths)

main()