import json
import os

def read_function_names(path):
  '''
  Reads the JSON file specified by the path and outputs a list of function
  names and arguments corresponding to each function name.

  Example:
  {
    "functions": [
      {
        "name": "test_func",
        "args": [
          "arg1", "arg2"
        ]
      }
  }

  yields

  names = ['test_func']
  args = {
    'test_func': ['arg1', 'arg2']
  }
  '''
  f = open(path, 'r')
  json_data = json.load(f)
  f.close()

  names = []
  args = {}
  try:
    for func in json_data['functions']:
      names.append(func['name'])
      args[func['name']] = func['args']
  except Exception:
    print('Note: function names JSON file has incorrect format:', os.path.abspath(path))
    print('Ensure file follows the format:', """
      {
        "functions": [
          {
            "name": "[function name]",
            "args": [
              "arg1", "arg2", ... 
            ]
          },
          {
            "name": "[another function name]",
            "args": [
              "arg1", "arg2", ... 
            ]
          }
        ]
      }
    """)
  return args