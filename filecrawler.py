import os

def crawlDirectory(path, ignoreList):
  path = os.path.abspath(path)
  paths = []
  for entry in os.scandir(path):
    if os.path.basename(entry) in ignoreList:
      continue

    if entry.is_dir():
      res = crawlDirectory(os.path.join(path, entry.name), ignoreList)
      paths = paths + res
    else:
      paths.append(os.path.join(path, entry.name))

  return paths