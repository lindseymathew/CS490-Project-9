#!/usr/bin/env python3

from astconverter import convert_ast_to_json
from filecrawler import crawl_directory
from ignore import create_ignore_dict
from astgen.parser import generate_file_ast

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
    ast_json = convert_ast_to_json(ast)
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
      # Create file output structure that matches project structure in
      # output folder.
      rel_path = os.path.relpath(path, project_path)
      if rel_path == '.':
        rel_path = os.path.basename(project_path)
      filename_extension = os.path.splitext(rel_path)

      # Given an example python file: test.py, the corresponding output file is
      # named 'test_py_output' or '<base file name>_<extension type>_output>'
      output_file = filename_extension[0] + '_' + filename_extension[1][1:] + '_output'
      output_dir = os.path.join(output_path, output_file)

      # Create the directories for the output file to exist.
      os.makedirs(os.path.dirname(output_dir), exist_ok = True)
      
      # Output the JSON file.
      output_file = open(output_dir, 'w')
      output_file.write(json.dumps(ast_json, indent = 2))
      output_file.close()
main()
