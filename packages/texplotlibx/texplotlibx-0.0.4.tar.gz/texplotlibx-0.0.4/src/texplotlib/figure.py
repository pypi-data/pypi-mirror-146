from collections.abc import Iterable
import csv
import subprocess

from .label import _tpl_label
from .attribute import _tpl_single_variable
from .curve import _tpl_curve
from .legend import _tpl_legend
from .strutils import _savetext, _compactify
from .logmodes import _tpl_logmodes


class figure:
  PDF_COMPILE_CMD = "pdflatex -halt-on-error -interaction nonstopmode TEXFILE | grep '^!.*' -A200 --color=always"

  def __init__(self, figsize: tuple = None):
    if figsize is None:
      figsize = (8, 5)
    self.__figsize: tuple = figsize
    self.__curves: list[_tpl_curve] = []
    self.__xlabel: _tpl_label = _tpl_label(token="xlabel")
    self.__ylabel: _tpl_label = _tpl_label(token="ylabel")
    self.__xprecision: _tpl_single_variable = _tpl_single_variable(token="precision")
    self.__yprecision: _tpl_single_variable = _tpl_single_variable(token="precision")
    self.__legend: _tpl_legend = _tpl_legend()
    self.__type: str = "xy"
    self.__logmodes: _tpl_logmodes = _tpl_logmodes()
    self.__additional_axis_cmds: list[str] = []
    self.__floating_x_ticks = False
    self.__floating_y_ticks = False

  def plot(self, x: Iterable, y: Iterable, xerror: Iterable = None, yerror: Iterable = None,
           label: str = None, color: str = None):
    if len(x) != len(y):
      print("x and y must be of same length (%d != %d)" % (len(x), len(y)))
      return
    self.__curves.append(_tpl_curve(x, y, xerror, yerror, label, color))

  def plotcsv(self, filename: str, xcolname: str, ycolname: str, xerrcolname: str = None, yerrcolname: str = None,
              label: str = None, color: str = None):
    with open(filename, "r") as f:
      csvreader = csv.reader(f)
      data = dict()
      for d in list(map(list, zip(*([x for x in csvreader if x != []])))):
        data[d[0]] = d[1:]

      def error(axis: str, v: str):
        print("Cannot find %s-key \"%s\" in csv file %s" % (axis, v, filename))
        print("Found the following data:")
        print(data)
      if xcolname not in data.keys():
        error("x", xcolname)
        return
      if ycolname not in data.keys():
        error("y", ycolname)
        return
      if xerrcolname is not None and xerrcolname not in data.keys():
        error("x error", xerrcolname)
        return
      if yerrcolname is not None and yerrcolname not in data.keys():
        error("y error", yerrcolname)
        return
      xerr = data[xerrcolname] if xerrcolname in data.keys() else None
      yerr = data[yerrcolname] if yerrcolname in data.keys() else None

      self.__curves.append(_tpl_curve(data[xcolname], data[ycolname], xerr, yerr, label, color))

  def savefig(self, filename: str):
    DEFAULT_SUFFIX = "tex"
    splitfile = filename.split(".")
    suffix = splitfile[-1] if len(splitfile) != 1 else None
    if suffix is None:
      suffix = DEFAULT_SUFFIX
      filename += "." + DEFAULT_SUFFIX
      print(f"No file-suffix specified. Assuming {DEFAULT_SUFFIX}.")
    if suffix.lower() == "tex":
      texstr = self.__create_tex()
      _savetext(filename, texstr)
    elif suffix.lower() == "tikz":
      tikzstr = self.__create_tikz()
      _savetext(filename, tikzstr)
    elif suffix.lower() == "pdf":
      texfilename = ".".join(filename.split(".")[:-1]) + ".tex"
      texstr = self.__create_tex()
      _savetext(texfilename, texstr)
      subprocess.run(self.__class__.PDF_COMPILE_CMD.replace("TEXFILE", texfilename).split())
    else:
      print("File type \"%s\" not supported!" % suffix)

  def set_xlabel(self, label: str):
    self.__xlabel.text = label

  def set_ylabel(self, label: str):
    self.__ylabel.text = label

  def set_xprecision(self, precision: int):
    self.__xprecision.val = precision

  def set_yprecision(self, precision: int):
    self.__yprecision.val = precision

  def set_legend_position(self, pos: str):
    self.__legend.pos.val = pos

  def set_plottype(self, type: str = 'xy'):
    """
    Possibilities:
      'bar', 'ybar', 'hist', 'histogram' ... bar chart
      'interval' ... interval plot (similar to histogram)
    """
    if type == 'bar' or type == 'ybar' or type == 'hist' or type == 'histogram':
      type = 'ybar'
    self.__type = type

  def set_logmode(self, mode: str = None):
    self.__logmodes.set_mode(mode)

  def add_axis_command(self, cmd: str):
    self.__additional_axis_cmds.append(cmd)

  def set_floating_x_ticks(self, floating: bool = False):
    self.__floating_x_ticks = floating

  def set_floating_y_ticks(self, floating: bool = False):
    self.__floating_y_ticks = floating

  def __create_tex(self):
    preable_cmd = """\\documentclass[tikz]{standalone}\n
\\usepackage{pgfplots}
\\pgfplotsset{compat=newest}\n
\\begin{document}\n\n"""

    tikz_cmd = self.__create_tikz(True)

    end_cmd = "\n\\end{document}"

    return preable_cmd + tikz_cmd + end_cmd

  def __create_tikz(self, include_begintikz: bool = True):
    begintikz_cmd = "\\begin{tikzpicture}\n" if include_begintikz else ""

    xticklabelstyle = f"""x tick label style={{
    /pgf/number format/.cd,
    fixed,
    fixed zerofill,
    {self.__xprecision}
    /tikz/.cd
  }},""" if self.__xprecision.val is not None or self.__floating_x_ticks else "%x tick label style"

    yticklabelstyle = f"""y tick label style={{
    /pgf/number format/.cd,
    fixed,
    fixed zerofill,
    {self.__yprecision}
    /tikz/.cd
  }},""" if self.__yprecision.val is not None or self.__floating_y_ticks else "%y tick label style"

    body_cmd = f"""\\begin{{axis}}[
  {self.__xlabel}
  {self.__ylabel}
  {xticklabelstyle}
  {yticklabelstyle}
  tick label style={{
    font=\\large
  }},
  label style={{
    font=\\large
  }},
  {self.__legend.pos}
  legend cell align={{left}},
  grid=minor,
  grid style=dotted,
  scale only axis,
  {"ybar," if self.__type == 'ybar' else "%ybar"}
  {"area style," if self.__type == 'interval' else "%area style"}
  {self.__logmodes.x}
  {self.__logmodes.y}"""
    body_cmd += ''.join(["\n  " + x + "," for x in self.__additional_axis_cmds])
    body_cmd += "\n]\n\n"

    xerrorstr = ["x dir=both,\n  x explicit,"
                 if c.xerror is not None else "%x error options" for c in self.__curves]
    yerrorstr = ["y dir=both,\n  y explicit,"
                 if c.yerror is not None else "%y error options" for c in self.__curves]
    errorstr = [f"""
  error mark options={{
    rotate=90,
    mark size=4pt,
    {"draw=%s" % c.color.value() if c.color.value() is not None and self.__type == 'ybar' else "%draw"}
  }}""" if c.xerror is not None or c.yerror is not None else "%error mark options" for c in self.__curves]

    tables = []
    for c in self.__curves:
      table = f"\n  {'x':>8}, {'y':>8}"
      if c.xerror is None and c.yerror is None:
        table += "\n"
        table += "\n".join([f"  {cx:8}, {cy:8}" for cx, cy in zip(c.x, c.y)])
      elif c.xerror is not None and c.yerror is None:
        table += f", {'dx':>8}\n"
        table += "\n".join([f"  {cx:8}, {cy:8}, {cdx:8}" for cx, cy, cdx in zip(c.x, c.y, c.xerror)])
      elif c.xerror is None and c.yerror is not None:
        table += f", {'dy':>8}\n"
        table += "\n".join([f"  {cx:8}, {cy:8}, {cdy:8}" for cx, cy, cdy in zip(c.x, c.y, c.yerror)])
      elif c.xerror is not None and c.yerror is not None:
        table += f", {'dx':>8}, {'dy':>8}\n"
        table += "\n".join([f"  {cx:8}, {cy:8}, {cdx:8}, {cdy:8}"
                            for cx, cy, cdx, cdy in zip(c.x, c.y, c.xerror, c.yerror)])
      table += "\n"
      tables.append(table)

    plot_cmd = [f"""\\addplot+[
  {c.color if c.color.value() is not None and self.__type != 'ybar' else f"%color"}
  {"fill=%s!30," % c.color.value() if c.color.value() is not None and self.__type == 'ybar' else f"%fill"}
  {"draw=%s," % c.color.value() if c.color.value() is not None and self.__type == 'ybar' else f"%draw"}
  {"only marks," if self.__type != 'ybar' else f"%only marks"}
  {"error bars/.cd," if c.xerror is not None or c.yerror is not None else "%error options"}
  {xerrorstr[i]}
  {yerrorstr[i]}
  {errorstr[i]}
  {"ybar interval," if self.__type == 'interval' else "%ybar interval"}
] table [
  x=x,
  {"x error=dx," if c.xerror is not None else "%x error"}
  y=y,
  {"y error=dy," if c.yerror is not None else "%y error"}
  col sep=comma
] {{{tables[i]}}};
{c.label}
""" for i, c in enumerate(self.__curves)]

    post_cmd = "\n\\end{axis}\n"

    endtikz_cmd = "\\end{tikzpicture}\n" if include_begintikz else ""

    return begintikz_cmd \
      + body_cmd \
      + "\n".join([_compactify(pc) for pc in plot_cmd]) \
      + post_cmd \
      + endtikz_cmd
