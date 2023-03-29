import json

def read_function_names(path):
  f = open(path, 'r')
  json_data = json.load(f)
  f.close()

  names = []
  args = {}
  for func in json_data['functions']:
    names.append(func['name'])
    args[func['name']] = func['args']
  return names, args