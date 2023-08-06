from .attribute import _tpl_single_variable


class _tpl_logmodes:
  def __init__(self):
    self.x = _tpl_single_variable(None, 'xmode')
    self.y = _tpl_single_variable(None, 'ymode')

  def set_mode(self, mode: str):
    if mode == 'linear' or mode == '' or mode is None:
      self.x.val = None
      self.y.val = None
    if 'x' in mode:
      self.x.val = 'log'
    if 'y' in mode:
      self.y.val = 'log'
