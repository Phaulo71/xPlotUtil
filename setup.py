from cx_Freeze import setup, Executable
import os
import sys
import scipy

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

includefiles_list=[]
scipy_path = os.path.dirname(scipy.__file__)
includefiles_list.append(scipy_path)

base = 'Win32GUI' if sys.platform == 'win32' else None

options = {"packages": ["os", "idna", "numpy", "spec2nexus"], "include_files": includefiles_list, "includes": ['multiprocessing.process']}

setup(name="xPlotUtil",
      version="0.1",
      options={"build_exe": options},
      description="Allows fitting and plotting of point data from spec file.",
      executables=[Executable("xPlotUtil/PlotWindow.py", base=base)])