import os

def crawl_directory(path, ignore_list):
  path = os.path.abspath(path)
  paths = []
  for entry in os.scandir(path):
    if os.path.basename(entry) in ignore_list:
      continue

    if entry.is_dir():
      res = crawl_directory(os.path.join(path, entry.name), ignore_list)
      paths = paths + res
    else:
      paths.append(os.path.join(path, entry.name))

  return paths
