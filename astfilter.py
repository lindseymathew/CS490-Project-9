class ASTFilter():
  def __init__(self, function_names, args):
    self.function_names = function_names
    self.func_args = args

  def run(self, ast):
    return self.filter_ast(ast)

  def filter_ast(self, ast_nodes):
    if not self.function_names:
      return self.ast
    
    ast_nodes['imports'] = list(filter(lambda x: self.search_imports(x), ast_nodes['imports']))
    ast_nodes['import_froms'] = list(filter(lambda x: self.search_imports(x), ast_nodes['import_froms']))

    new_calls = []
    for call in ast_nodes['calls']:
      if self.reduce_call(call):
        new_calls.append(call)
    ast_nodes['calls'] = new_calls

    new_function_defs = []
    for function_def in ast_nodes['function_defs']:
      if self.reduce_function_def(function_def):
        new_function_defs.append(function_def)

    ast_nodes['function_defs'] = new_function_defs
    return ast_nodes

  def search_imports(self, imports_ast):
    for name in imports_ast['names']:
      if name['name'] in self.function_names:
        return True
    return False

  def search_call_name(self, name_obj):
    if isinstance(name_obj, str):
      return name_obj if name_obj in self.function_names else None
    
    if name_obj['attribute'] in self.function_names:
      return name_obj['attribute']
    
    return self.search_call_name(name_obj['object'], function_names)

  def filter_call_args(self, call_ast, func_args):
    args = []
    for arg in call_ast['args']:
      if isinstance(arg, dict) and 'type' in arg.keys() and arg['type'] == 'call':
        args.append(arg)
    call_ast['args'] = args

    keywords = []
    for keyword in call_ast['keywords']:
      if keyword['keyword'] in func_args:
        keywords.append(keyword)
    call_ast['keywords'] = keywords

  def reduce_call(self, call_ast):
    call_name = self.search_call_name(call_ast['function'])
    if call_name:
      self.filter_call_args(call_ast, self.func_args[call_name])
      return True
    
    args = []
    for arg in call_ast['args']:
      if isinstance(arg, dict) and 'type' in arg.keys():
        if arg['type'] == 'call' and self.reduce_call(arg):
          args.append(arg)
    
    keywords = []
    for keyword in call_ast['keywords']:
      if keyword['keyword'] in self.function_names:
        keywords.append(keyword)
      elif isinstance(keyword['value'], dict) and keyword['value']['type'] == 'call':
        if self.reduce_call(keyword['value']):
          keywords.append(keyword)

    call_ast['args'] = args
    call_ast['keywords'] = keywords
    return len(args) > 0 or len(keywords) > 0

  def reduce_function_def(self, function_def_ast):
    if function_def_ast['name'] in self.function_names:
      return True
    
    calls = []
    for call in function_def_ast['calls']:
      if self.reduce_call(call):
        calls.append(call)
    
    function_defs = []
    for function_def in function_def_ast['function_defs']:
      if reduce_function_def(function_def):
        function_defs.append(function_def)
    
    function_def_ast['calls'] = calls
    function_def_ast['function_defs'] = function_defs
    return len(calls) > 0 or len(function_defs) > 0

