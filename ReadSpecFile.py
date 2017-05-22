#!/usr/bin/env python

"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.

"""

# --------------------------------------------------------------------------------------#
from __future__ import unicode_literals
from pylab import *
from matplotlib.backends import qt_compat
import os
from GaussianFit import GaussianFitting
use_pyside = qt_compat.QT_API == qt_compat.QT_API_PYSIDE
if use_pyside:
    from PySide import QtGui, QtCore
else:
    from PyQt4 import QtGui, QtCore
from spec2nexus.spec import SpecDataFile
# --------------------------------------------------------------------------------------#

class ReadSpec:

    def __init__ (self, parent=None):
        self.dockedOpt = parent
        self.myMainWindow = self.dockedOpt.myMainWindow

    def loadScans(self, scans):
        self.scans = scans
        scanKeys = self.scans.keys()

        scanKeys.sort(key=int)  # Sorts the scans in alphabetical order
        for scan in scanKeys:
            PValue = 'PVvalue #' + str(scans[scan].scanNum)
            self.dockedOpt.specDataList.addItem(PValue)
            """
            scanItem = QtGui.QTableWidgetItem(str(scans[scan].scanNum))
            self.scanList.setItem(row, SCAN_COL, scanItem)
            cmdItem = QtGui.QTableWidgetItem(scans[scan].scanCmd)
            print(scans[scan].scanCmd)
            nPointsItem = QtGui.QTableWidgetItem(str(len(scans[scan].data_lines)))
            self.scanList.setItem(row, NUM_PTS_COL, nPointsItem)
            row +=1"""

    def currentScan(self):
        scan = str(self.dockedOpt.specDataList.currentRow() + 1)
        self.dockedOpt.rdOnlyScanSelected.setText("PvValue #" + scan)
        print(self.scans[scan].raw)
        print(self.scans[scan].data)
        print(self.scans[scan].comments)
        print(self.scans[scan].data_lines)
        print(self.scans[scan].data["Ion_Ch_5"])
