#!/usr/bin/env python3

from asttojson import convert_ast_to_json
from filecrawler import crawl_directory
from ignore import create_ignore_list
from parser import generate_file_ast

import ast
import json
import os
import sys

def main():
  if len(sys.argv) < 3:
    print('Python project path not found!\nUsage: ./main.py <relative/absolute project path> <output path>')
    return
  
  project_path = sys.argv[1]
  print('Path entered:', os.path.abspath(project_path))

  file_paths = crawl_directory(project_path, create_ignore_list())
  file_ast = generate_file_ast(file_paths)

  results = []
  for ast in file_ast:
    results.append(convert_ast_to_json(ast))

  output_path = sys.argv[2]
  if len(results) > 0:
    if not os.path.exists(output_path):
      os.makedirs(output_path)
    for idx, result in enumerate(results):
      if len(result) > 0:
        output_file = open(output_path + '/' + str(idx), 'w')
        output_file.write(json.dumps(result, indent = 2))
        output_file.close()
main()
