import os
import re

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
