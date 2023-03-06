import os

def crawlDirectory(path, ignoreList):
  path = os.path.abspath(path)
  paths = []
  for root, dirs, files in os.walk(path):
    if os.path.basename(root) in ignoreList:
      continue
    
    for filename in files:
      if os.path.basename(filename) not in ignoreList:
        paths.append(os.path.join(root, filename))

    for dir in dirs:
      res = crawlDirectory(dir, ignoreList)
      paths = paths + res
  return paths