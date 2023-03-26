#!/usr/bin/env python3

from astconverter import AstConverter
from filecrawler import crawl_directory
from ignore import create_ignore_dict
from output import create_output_directory
from parser import generate_file_ast

import ast
import json
import os
import sys

def main():
  if len(sys.argv) < 3:
    print('Error: Not enough arguments\nUsage: ./main.py <relative/absolute project path> <output directory>')
    return
  
  project_path = os.path.abspath(sys.argv[1])
  if not os.path.exists(project_path):
    print('Error: Invalid path entered -', project_path)
    return
  else:
    print('Path entered:', project_path)
  
  output_path = os.path.abspath(sys.argv[2])
  if os.path.exists(output_path):
    print('Error: Output directory already exists -', output_path)
    return

  # Retrieve file paths that are not 'ignored' by the .ignore file.
  file_paths = crawl_directory(project_path, create_ignore_dict())

  # Generate file AST for each path.
  file_ast = generate_file_ast(file_paths)

  # Convert each AST to a JSON string.
  results = []
  for [path, ast] in file_ast:
    converter = AstConverter()
    ast_json = converter.run(ast)
    results.append([path, ast_json])

  # Create the output directory if there is something to output.
  if len(results) > 0:
    os.makedirs(output_path)
    print('Output path entered:', output_path)
  else:
    print('Note: Specified project directory resulted in empty output.')
    return

  # Each file that is found is output under the output directory
  # The naming convention of the output files is
  # [0, number of files with valid JSON data).
  for [path, ast_json] in results:
    if len(ast_json) > 0:
      # Create the output directory
      output_dir = create_output_directory(path, project_path, output_path)

      # Output the JSON file.
      output_file = open(output_dir, 'w')
      output_file.write(json.dumps(ast_json, indent = 2))
      output_file.close()
main()
