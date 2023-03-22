import os
import re

"""Crawls the directory starting at the path to find file paths that are valid.

crawl_directory traverses the 'path' in DFS fashion and identifies all the files that are
not specified by ignore_list either via pattern or specific path.

Usage:
└── my_project
    ├── Test/
    │   └── test.py
    ├── Help/
        └── helpers.py
    └── configs.py

ignore_list = {}
ignore_list['paths'] = ['my_project/configs.py']
ignore_list['patterns'] = ['Hel.*']

crawl_directory(my_project, ignore_list) -> ['my_project/Test/test.py']
"""
def crawl_directory(path, ignore_list):
  path = os.path.abspath(path)
  paths = []

  if os.path.isfile(path):
    if path in ignore_list['paths']:
      return []
    
    for pattern in ignore_list['patterns']:
      if re.search(pattern, path) != None:
        return []
    return [path]

  for entry in os.scandir(path):
    if os.path.abspath(entry) in ignore_list['paths']:
      continue
      
    cont = False
    for pattern in ignore_list['patterns']:
      if re.search(pattern, os.path.abspath(entry)) != None:
        cont = True
        break
    
    if cont:
      continue

    if entry.is_dir():
      res = crawl_directory(os.path.join(path, entry.name), ignore_list)
      paths = paths + res
    else:
      paths.append(os.path.join(path, entry.name))

  return paths
