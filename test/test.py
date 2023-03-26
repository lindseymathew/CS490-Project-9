import ast as a
import time as t
import time.stoptime as stop
from math import sin as s, cos as c

def return_ast():
  def test():
    return None
  return a

def return_None(x, test=3):
  if test > 2:
    return return_None(test - 1)
  elif test > 0:
    return return_None(test - 1)
  return None

print(return_ast().walk(return_None(3, x = 4)))
