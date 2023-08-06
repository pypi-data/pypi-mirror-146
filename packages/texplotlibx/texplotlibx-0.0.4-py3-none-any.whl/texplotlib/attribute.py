from .strutils import _escape_characters


class _tpl_attribute:
  def __init__(self, token: str = None, function_mode: bool = False):
    self.token = token
    if function_mode:
      self.strmethod = self.__class__.__as_function
    else:
      self.strmethod = self.__class__.__as_variable

  def __str__(self):
    return self.strmethod(self)

  def value(self):
    return None

  def __as_variable(self):
    v = self.value()
    if v is None:
      return f"%{self.token}"
    elif self.token is None:
      return str(v)
    else:
      return self.token + "=" + str(v) + ","

  def __as_function(self):
    v = self.value()
    if v is None:
      return f"%{self.token}"
    elif self.token is None:
      return str(v)
    else:
      return "\\" + self.token + "{" + str(v) + "};"


class _tpl_single_variable(_tpl_attribute):
  def __init__(self, value=None, token: str = None, function_mode: bool = False):
    self.val = value
    super().__init__(token, function_mode)

  def value(self):
      return _escape_characters(self.val) if type(self.val) is str else self.val
