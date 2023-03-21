import os
import re

def create_ignore_list():
  output_dict = {'paths': [], 'patterns': []}
  try:
    with open('.ignore') as f:
      output = []
      name_patterns = []
      for line in f.read().splitlines():
        if line.startswith('pattern:'):
          pattern = line[8:]
          pattern = re.escape(pattern)
          pattern = pattern.replace('\\*', '.*').replace('\\?', '.')
          pattern = pattern
          name_patterns.append(pattern)
        else:
          output.append(os.path.abspath(line))
      output_dict['paths'] = output
      output_dict['patterns'] = name_patterns
  except Exception as e:
    print(e)
    f = open('.ignore', 'w')
    f.write('./.ignore')
    f.close()
    output_dict['paths'] = [os.path.abspath('./ignore')]
  
  return output_dict
