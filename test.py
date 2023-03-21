import ast as a

def return_None():
  return None

print(a.walk(return_None()))
