#!/usr/bin/env python

"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.

"""

# --------------------------------------------------------------------------------------#
from __future__ import unicode_literals
from pylab import *
from matplotlib.backends import qt_compat
from GaussianFit import GaussianFitting
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
        self.gausFit = GaussianFitting(self)
        self.specFileOpened = False
        self.specFileName = None

        # L information
        self.L = []
        self.lElement = 0
        self.lMax = 0
        self.lMin = 0

    def loadScans(self, scans):
        self.scans = scans
        scanKeys = self.scans.keys()

        scanKeys.sort(key=int)  # Sorts the scans in alphabetical order
        for scan in scanKeys:
            PValue = 'PVvalue #' + str(scans[scan].scanNum)
            self.dockedOpt.specDataList.addItem(PValue)

    def currentScan(self):
        scan = str(self.dockedOpt.specDataList.currentRow() + 1)
        self.dockedOpt.openFile()

        # Making sure the file of the PVvalue has been opened
        try:
            if os.path.isfile(self.dockedOpt.fileName) == True:
                # Getting the L information for the particular PVValue
                self.L = self.scans[scan].data["L"]
                self.lMin = self.L[0]
                self.lMax = self.L[-1]
                k = self.scans[scan].G["G1"].split(" ")
                self.lElement = float(k[2])
        except TypeError and RuntimeError and KeyError:
            print("Please make sure the PVValue file has the information on the file.")

    # ------------------------------------------------------------------------------------#
    def openSpecFile(self):
        if self.specFileOpened == False:
            self.openSpecDialog()
        elif self.specFileOpened == True:
            response = self.dockedOpt.msgApp("Open New Spec File", "Would you like to open a new spec file?")
            if response == "Y":
                self.openSpecDialog()

    def openSpecDialog(self):
        """This method allows the user to open the spec file """
        filters = "Spec files (*.spec);;Python files (*.py)"
        selectedFilter = "Spec files (*.spec);;Python files (*.py)"
        self.specFileName = QtGui.QFileDialog.getOpenFileName(self.myMainWindow, "Open Spec File", filters, selectedFilter)

        # Makes sure a file has been opened
        if os.path.isfile(self.specFileName) == True:
            self.dockedOpt.mainOptions.close()
            self.gausFitStat = False
            self.LFitStat = False
            self.dockedOpt.DockMainOptions()
            self.dockedOpt.rdOnlyFileName.setText(self.specFileName)
            self.dockedOpt.rdOnlyFileName.setStatusTip(self.specFileName)
            self.specFile = SpecDataFile(self.specFileName)
            self.dockedOpt.specDataList.clear()
            self.loadScans(self.specFile.scans)
            self.specFileOpened = True
            self.dockedOpt.fileOpened = False