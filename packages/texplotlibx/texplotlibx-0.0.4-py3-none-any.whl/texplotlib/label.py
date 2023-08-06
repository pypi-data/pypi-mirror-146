from .attribute import _tpl_attribute
from .strutils import _escape_characters


class _tpl_label(_tpl_attribute):
  def __init__(self, text: str = None, token: str = None):
    self.text = text
    super().__init__(token)

  def value(self):
    return _escape_characters(self.text)
