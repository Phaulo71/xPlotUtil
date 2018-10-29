from cx_Freeze import setup, Executable
import os
import sys
import scipy
import matplotlib


includefiles_list=[]
scipy_path = os.path.dirname(scipy.__file__)
includefiles_list.append(scipy_path)
matplotlib_path = os.path.dirname(matplotlib.__file__)
includefiles_list.append(matplotlib_path)
os_path = os.path.dirname(os.__file__)

# This is required by windows to create the executable folder.
os.environ['TCL_LIBRARY'] = r'C:\Program Files\Python35-32\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Program Files\Python35-32\tcl\tk8.6'
includefiles_list.append(os_path)
includefiles_list.append("graph.ico")

base = 'Win32GUI' if sys.platform == 'win32' else None

options = {"packages": ["os", "idna", "numpy", "spec2nexus", "lmfit", "matplotlib", ],
           "include_files": includefiles_list, "includes": ['os', 'lmfit.models']}

setup(name="xPlotUtil",
      version="0.1",
      options={"build_exe": options},
      description="Allows fitting and plotting of point data from spec file.",
      executables=[Executable("xPlotUtil/PlotWindow.py", icon='graph.ico', base=base, shortcutDir='xPlotUtil')])