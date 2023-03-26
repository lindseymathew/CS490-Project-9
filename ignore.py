import os
import re

def create_ignore_dict():
  '''Returns a dictionary containing paths and regex patterns that should be
  ignored by the file crawler. The ignore dictionary is created using the
  .ignore file. Paths can be relative or absolute, and ignored patterns are
  specified using the 'ignore:' prefix in the .ignore file.
  '''
  output_dict = {'paths': [], 'ignore': [], 'include': []}
  try:
    with open('.ignore') as f:
      output = []
      name_patterns = []
      include_patterns = []
      for line in f.read().splitlines():
        if line.startswith('ignore:'):
          # Convert wild card expressions such as '.gi*' into regex compatible
          # expressions
          pattern = line[7:]
          pattern = re.escape(pattern)
          pattern = pattern.replace('\\*', '.*').replace('\\?', '.')
          name_patterns.append(pattern)
        elif line.startswith('include:'):
          # Convert wild card expressions such as '.gi*' into regex compatible
          # expressions
          pattern = line[8:]
          pattern = re.escape(pattern)
          pattern = pattern.replace('\\*', '.*').replace('\\?', '.')
          include_patterns.append(pattern)
        else:
          output.append(os.path.abspath(line))
      output_dict['paths'] = output
      output_dict['ignore'] = name_patterns
      output_dict['include'] = include_patterns
  except Exception as e:
    # Do nothing if the file does not exist
    return output_dict

  return output_dict
