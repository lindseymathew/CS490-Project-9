import os
import re

def crawl_directory(path, ignore_list):
  '''Crawls the directory starting at the path to find file paths that are valid.

  crawl_directory traverses the 'path' in DFS fashion and identifies all the files that are
  not specified by ignore_list either via pattern or specific path.

  Example:
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
  '''

  path = os.path.abspath(path)
  paths = []

  # If the path is a file, check if specified in ignore_list.
  if os.path.isfile(path):
    if path in ignore_list['paths']:
      return []

    for pattern in ignore_list['ignore']:
      if re.search(pattern, path) != None:
        return []

    if len(ignore_list['include']) > 0:
      for pattern in ignore_list['include']:
        if re.search(pattern, path) != None:
          return [path]
      return []
    else:
      return [path]

  # If not file, crawl the directory and identify all the valid file paths
  # not specified in ignore_list.
  for entry in os.scandir(path):
    if os.path.abspath(entry) in ignore_list['paths']:
      continue
      
    cont = False
    for pattern in ignore_list['ignore']:
      if re.search(pattern, os.path.abspath(entry)) != None:
        cont = True
        break

    if cont:
      continue

    if entry.is_dir():
      res = crawl_directory(os.path.join(path, entry.name), ignore_list)
      paths = paths + res
    else:
      if len(ignore_list['include']) > 0:
        for pattern in ignore_list['include']:
          if re.search(pattern, os.path.abspath(entry)) != None:
            paths.append(os.path.join(path, entry.name))
            break
      else:
        paths.append(os.path.join(path, entry.name))

  return paths
