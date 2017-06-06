#!/usr/bin/env python

"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.

#C In some methods LFit or L refer to the Lattice Constant not RLU
"""

# --------------------------------------------------------------------------------------#
from __future__ import unicode_literals
from pylab import *
from matplotlib.backends import qt_compat
from GaussianFit import GaussianFitting
import os
from pathlib2 import Path
from GaussianFit import GaussianFitting
use_pyside = qt_compat.QT_API == qt_compat.QT_API_PYSIDE
if use_pyside:
    from PySide.QtGui import *
    from PySide.QtCore import *
else:
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *

from spec2nexus.spec import SpecDataFile
# --------------------------------------------------------------------------------------#

class ReadSpec:

    def __init__ (self, parent=None):
        self.dockedOpt = parent
        self.myMainWindow = self.dockedOpt.myMainWindow
        self.gausFit = GaussianFitting(self)
        self.specFileOpened = False
        self.specFileName = None

        # Initializing lattice information
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
        self.scan = str(self.dockedOpt.specDataList.currentRow() + 1)
        self.currentRow = self.dockedOpt.specDataList.currentRow()
        self.dockedOpt.openFile()
        self.myMainWindow.normalizeAction.setEnabled(True)

        # Making sure the file of the PVvalue has been opened
        try:
            if os.path.isfile(self.dockedOpt.fileName):
                self.normalizers = [] # Array that will contain possible normalizer
                # Getting the L information for the particular PVValue
                lattice = self.scans[self.scan].data["L"]

                self.lMin = lattice[0]
                self.lMax = lattice[-1]
                k = self.scans[self.scan].G["G1"].split(" ")
                self.lElement = float(k[2])
                self.getRLU()

                # Gets possible normalizer values
                for key in self.scans[self.scan].data.keys():
                    if key.find("Ion_Ch_") == 0:
                        self.normalizers.append(key)
                self.normalizers.sort()
        except TypeError or RuntimeError or KeyError:
            print("Please make sure the PVValue has the correct information in the spec file.")

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
        try:
            selectedFilter = "Spec files (*.spec)"
            self.specFileName, self.specFileFilter = QFileDialog.getOpenFileName(self.myMainWindow, "Open Spec File",
                                                                                 None, selectedFilter)
            self.dockedOpt.mainOptions.close()
            self.dockedOpt.DockMainOptions()
            self.myMainWindow.LatticeFitAction.setEnabled(False)

            # Makes sure a file has been opened
            if os.path.isfile(self.specFileName):
                self.dockedOpt.gausFitStat = False
                self.myMainWindow.normalizeAction.setEnabled(False)
                self.dockedOpt.LFitStat = False
                self.dockedOpt.normalizingStat = False
                self.dockedOpt.rdOnlyFileName.setText(self.specFileName)
                self.dockedOpt.rdOnlyFileName.setStatusTip(self.specFileName)
                self.specFile = SpecDataFile(self.specFileName)
                self.loadScans(self.specFile.scans)
                self.specFileOpened = True
                self.dockedOpt.fileOpened = False
                self.continueGraphingEachFit = True
        except:
            print("Please make sure the spec file has the correct format.")


    def getRLU(self):
        """This function gets the Lattice for the particular file, using the lattice max, lattice min and the
        number of points on each column for the raw data. """
        nRow, nCol = self.dockedOpt.fileInfo()  # nRows = points || nCol = bins
        if nRow != 0:
            adjustment = (self.lMax - self.lMin)/nRow
            self.Lattice = [] #  Initializing Lattice array
            self.Lattice.append(self.lMin)
            RLU = self.lMin
            count = 1
            while count < nRow:
                RLU += round(adjustment, 4)
                self.Lattice.append(round(RLU, 5))
                count += 1

    def NormalizerDialog(self):
        if self.dockedOpt.normalizingStat == False:
            self.normalizeDialog = QDialog(self.myMainWindow)
            dialogBox = QVBoxLayout()
            buttonLayout = QHBoxLayout()
            vBox = QVBoxLayout()

            groupBox = QGroupBox("Select normalizer")
            self.buttonGroup = QButtonGroup(groupBox)

            for norm in self.normalizers:
                normalizerRB = QRadioButton(norm)
                self.buttonGroup.addButton(normalizerRB, int(norm[-1]))
                vBox.addWidget(normalizerRB)

            groupBox.setLayout(vBox)

            ok = QPushButton("Ok")
            cancel = QPushButton("Cancel")

            cancel.clicked.connect(self.normalizeDialog.close)
            ok.clicked.connect(self.getNormalizer)

            buttonLayout.addWidget(cancel)
            buttonLayout.addStretch(1)
            buttonLayout.addWidget(ok)

            dialogBox.addWidget(groupBox)
            dialogBox.addLayout(buttonLayout)

            self.normalizeDialog.setWindowTitle("What was used to normalize?")
            self.normalizeDialog.setLayout(dialogBox)
            self.normalizeDialog.resize(250, 250)
            self.normalizeDialog.exec_()

    def getNormalizer(self):
        if self.buttonGroup.checkedId() != -1:
            self.normalizeDialog.close()
            for norm in self.normalizers:
                if norm.endswith(str(self.buttonGroup.checkedId())):
                    self.normalizer = self.scans[self.scan].data[norm]
                    print self.normalizer
                    self.dockedOpt.NormalizerOptionsTree()



