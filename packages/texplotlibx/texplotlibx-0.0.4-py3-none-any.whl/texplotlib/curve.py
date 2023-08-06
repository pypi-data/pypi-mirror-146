from collections.abc import Iterable
from .attribute import _tpl_single_variable


class _tpl_curve:
  __counter: int = 0

  def __init__(self, x: Iterable, y: Iterable, xerror: Iterable = None, yerror: Iterable = None,
               label: str = None, color: str = None):
    self.x = x
    self.y = y
    self.xerror = xerror
    self.yerror = yerror
    self.label = _tpl_single_variable(value=label, token="addlegendentry", function_mode=True)
    self.tablename = "table%d" % _tpl_curve.__counter
    self.__class__.__counter += 1
    self.color = _tpl_single_variable(value=color, token="color")
