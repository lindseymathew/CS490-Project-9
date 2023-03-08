#!/usr/bin/env python3

from astcrawler import traverse_ast
from filecrawler import crawl_directory
from parser import generate_file_ast

import ast
import sys
import os

def create_ignore_list():
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
  
  project_path = sys.argv[1]
  print('Path entered:', os.path.abspath(project_path))

  file_paths = crawl_directory(project_path, create_ignore_list())
  file_ast = generate_file_ast(file_paths)
  for ast in file_ast:
    traverse_ast(ast)
  
main()