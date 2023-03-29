import os

def create_output_directory(path, project_path, output_path):
  '''Creates the file structure of the output folder such that the output files
  match the structure of the input files.

  Example:

  Using the command: ./main.py ./my_project ./output

  └── my_project
      ├── Test/
      │   └── test.py
      ├── Help/
          └── helpers.py
      └── configs.py
  
  yields

  └── my_project
      ├── Test/
      │   └── test.py
      ├── Help/
          └── helpers.py
      └── configs.py
  
  └── output
      ├── Test/
      │   └── test_py_output
      ├── Help/
          └── helpers_py_output
      └── configs_py_output

  '''

  # Create file output structure that matches project structure in
  # output folder.
  rel_path = os.path.relpath(path, project_path)
  if rel_path == '.':
    rel_path = os.path.basename(project_path)
  filename_extension = os.path.splitext(rel_path)

  # Given an example python file: test.py, the corresponding output file is
  # named 'test_py_output' or '<base file name>_<extension type>_output>'
  output_file = filename_extension[0]
  if filename_extension[1][1:] == '':
    output_file = output_file + '_' + filename_extension[1][1:]
  output_file = output_file + '_output'
  output_dir = os.path.join(output_path, output_file)

  # Create the directories for the output file to exist.
  os.makedirs(os.path.dirname(output_dir), exist_ok = True)

  return output_dir
