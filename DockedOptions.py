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
use_pyside = qt_compat.QT_API == qt_compat.QT_API_PYSIDE
if use_pyside:
    from PySide import QtGui, QtCore
else:
    from PyQt4 import QtGui, QtCore
from spec2nexus.spec import SpecDataFile
from ReadSpecFile import ReadSpec


class DockedOption(QtGui.QDockWidget):

    def __init__ (self, parent=None):
        super(DockedOption, self).__init__(parent)
        self.fileName = None
        self.myMainWindow = parent
        self.readSpec = ReadSpec(self)
        self.gausFit = self.readSpec.gausFit

        self.onePeakStat = False
        self.twoPeakStat = False
        self.fileOpened = False

        # keep track of when the fit has been done
        self.gausFitStat = False
        self.LFitStat = False


        self.TT = [0][0] # 2D array where raw data is stored

    # --------------------------------------------------------------------------------------------#
    def DockMainOptions(self):
        """Function that creates the dockWidget, Graph Options for fitting one
        """
        self.mainOptions = QtGui.QDockWidget("Main Options", self)
        self.mainOptions.setFloating(False)
        self.mainOptions.setMaximumWidth(320)
        self.mainOptions.setMinimumWidth(320)
        self.mainOptions.setAllowedAreas(QtCore.Qt.RightDockWidgetArea | QtCore.Qt.LeftDockWidgetArea)

        layout = QtGui.QFormLayout()
        FileHLayout = QtGui.QHBoxLayout()
        PVLayout = QtGui.QHBoxLayout()
        BtnLayout = QtGui.QHBoxLayout()
        self.dataDockedWidget = QtGui.QWidget()

        self.FileNameRdOnlyBox()
        self.BrowseButton()
        self.GraphDataButton()
        self.SpecDataValueList()
        self.DataGraphingRawOptionsTree()

        FileHLayout.addWidget(self.fileNameLabel)
        FileHLayout.addWidget(self.rdOnlyFileName)
        FileHLayout.addStretch(1)
        FileHLayout.addWidget(self.BrowseBtn)

        PVLayout.addWidget(self.pvLabel)
        PVLayout.addWidget(self.rdOnlyScanSelected)
        PVLayout.addStretch(1)

        BtnLayout.addStretch(1)
        BtnLayout.addWidget(self.GraphDataBtn)

        layout.addRow(FileHLayout)
        layout.addRow(PVLayout)
        layout.setVerticalSpacing(20)
        layout.addRow(self.specDataList)
        layout.addRow(self.graphingOptionsTree)
        layout.addRow(BtnLayout)
        self.dataDockedWidget.setLayout(layout)
        self.mainOptions.setWidget(self.dataDockedWidget)

        # Adding the docked widget to the main window
        self.myMainWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.mainOptions)

    # -----------------------------------------------------------------------------------#
    def restoreMainOptions(self):
        if self.mainOptions.isVisible() == False:
            self.mainOptions.show()
    # ------------------------------------------------------------------------------------#
    def FileNameRdOnlyBox(self):
        """This method contains a QLineEdit and label that display the selected file
            next to the browse button"""
        self.rdOnlyFileName = QtGui.QLineEdit()
        self.rdOnlyFileName.setReadOnly(True)
        self.rdOnlyFileName.setTextMargins(0, 0, 10, 0)
        self.rdOnlyFileName.setFixedWidth(125)

        #For the Gaussioan Fit
        self.rdOnlyScanSelected = QtGui.QLineEdit()
        self.rdOnlyScanSelected.setReadOnly(True)
        self.rdOnlyScanSelected.setTextMargins(0, 0, 10, 0)
        self.rdOnlyScanSelected.setFixedWidth(250)

        # Label
        self.fileNameLabel = QtGui.QLabel()
        self.fileNameLabel.setText("File Name: ")

        # PvValue label
        self.pvLabel = QtGui.QLabel()
        self.pvLabel.setText("Scan: ")

    # ------------------------------------------------------------------------------------#
    def WhichPeakGaussianFit(self):
        """This function calls on the appropriate method, depending on the amount of peaks"""
        if self.FileError() == False and  self.gausFitStat == False:
            chosePeak = self.PeakDialog()
            if (chosePeak == 'One'):
                self.gausFit.gausOnePeakInputDialog()
            elif (chosePeak == 'Two'):
                self.gausFit.gausTwoPeakInputDialog()

    # -----------------------------------------------------------------------------------#
    def openFile(self):
        if self.fileOpened == False:
            self.openDialog()
        elif self.fileOpened == True:
            response = self.msgApp("Open New Spec File", "Would you like to open a new spec file?")
            if response == "Y":
                self.openDialog()
                self.gausFitStat = False
                self.LFitStat = False

    def openDialog(self):
        """This method allows the user to open the spec file """
        self.rdOnlyScanSelected.setText("")
        filters = "All files (*.*);;Python files (*.py)"
        selectedFilter = "All files (*.*);;Python files (*.py)"
        self.fileName = QtGui.QFileDialog.getOpenFileName(self, "Open file for PVvalue #"
                                                          + str(self.specDataList.currentRow() + 1)
                                                          , filters, selectedFilter)

        # Makes sure a file has been opened
        if os.path.isfile(self.fileName) == True:
            self.gausFitStat = False
            self.LFitStat = False
            self.rdOnlyScanSelected.setStatusTip(self.fileName)
            self.rdOnlyScanSelected.setText(self.fileName)
            self.fileOpened = True

    # -----------------------------------------------------------------------------------#
    def PeakDialog(self):
        """Method that allows the user to choose which peak they are fitting"""
        peakList = ['One', 'Two']
        text, ok = QtGui.QInputDialog.getItem(self, 'Peak Fit', 'Choose Peak: ', peakList)

        if ok:
            return text

    # ------------------------------------------------------------------------------------#
    def msgApp(self, title, msg):
        userInfo = QtGui.QMessageBox.question(self, title, msg, QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

        if userInfo == QtGui.QMessageBox.Yes:
            return "Y"
        if userInfo == QtGui.QMessageBox.No:
            return "N"
        self.close()

    # ------------------------------------------------------------------------------------#
    def fileInfo(self):
        """This method is used to get the rows and columns of the data. It also sets the
        array with the raw data, which is the TT"""
        data = np.loadtxt(open(self.fileName))

        nRow = data.shape[0]  # Gets the number of rows
        nCol = data.shape[1]  # Gets the number of columns
        x = 0
        for f in range(nCol):
            if (np.mean(data[:, f]) == 0):
                break
            else:
                x += 1
        nCol = x

        self.TT = np.zeros((nRow, nCol))

        for i in range(nCol):
            self.TT[:, i] = data[:, i]

        return nRow, nCol

    # ------------------------------------------------------------------------------------#
    def BrowseButton(self):
        """Function that creates a browse method, connects to the openFile() method"""
        # Button next to the FileNameRdOnly label and LineEdit
        self.BrowseBtn = QtGui.QPushButton('Browse', self)
        self.BrowseBtn.clicked.connect(self.readSpec.openSpecFile)
        self.BrowseBtn.setStatusTip("Browse and open an existing file")

    def GraphDataButton(self):
        """Function that creates a graph button, connects to the GraphData() method"""
        self.GraphDataBtn = QtGui.QPushButton('Graph', self)
        self.GraphDataBtn.setStatusTip("Graphs the checked boxes")
        self.GraphDataBtn.clicked.connect(self.plottingFits)

    # --------------------------------------------------------------------------------------------#
    def SpecDataValueList(self):
        """This list displays the values/scans of the spec file
        """
        self.specDataList = QtGui.QListWidget()
        self.specDataList.itemDoubleClicked.connect(self.readSpec.currentScan)

    # --------------------------------------------------------------------------------------------#
    def FileError(self):
        if self.fileName is "" or self.fileName is None:
            QtGui.QMessageBox.warning(self, "Error - No File", "There is no data to graph."
                                                               " Make sure a file has been open.")
            return True
        else:
            if os.path.isfile(self.fileName) == False:
                QtGui.QMessageBox.warning(self, "Error - No File", "There is no data to graph."
                                                                   " Make sure a file has been open.")
                return True
            else:
                if self.rdOnlyScanSelected.text() == "":
                    QtGui.QMessageBox.warning(self, "Error", "Please select a PVvalue.")
                else:
                    return False

    # --------------------------------------------------------------------------------------------#
    def DataGraphingRawOptionsTree(self):
        """This method initializes the tree withthe raw data
        """
        # Initialization of the main tree
        self.graphingOptionsTree = QtGui.QTreeWidget()
        self.graphingOptionsTree.setHeaderLabel(QtCore.QString("Graphing Options"))

        """Initialization of the top level Fits"""
        # Raw Data Top Branch
        self.rawDataTopBranch = QtGui.QTreeWidgetItem(self.graphingOptionsTree)
        self.rawDataTopBranch.setText(0, "Raw Data")
        self.rawDataTopBranch.setFlags(self.rawDataTopBranch.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)

        """Raw Data Children"""
        # Color Graph
        self.colorGraphBranch = QtGui.QTreeWidgetItem(self.rawDataTopBranch)
        self.colorGraphBranch.setText(0, "Color Graph")
        self.colorGraphBranch.setFlags(self.colorGraphBranch.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
        self.colorGraphBranch.setCheckState(0, QtCore.Qt.Unchecked)

        # Line Graph in L-Constant
        self.lineGraphLBranch = QtGui.QTreeWidgetItem(self.rawDataTopBranch)
        self.lineGraphLBranch.setText(0, "Line Graph (L-Constant)")
        self.lineGraphLBranch.setFlags(self.lineGraphLBranch.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
        self.lineGraphLBranch.setCheckState(0, QtCore.Qt.Unchecked)

        # Line Graph in L-Constant
        self.lineGraphBinsBranch = QtGui.QTreeWidgetItem(self.rawDataTopBranch)
        self.lineGraphBinsBranch.setText(0, "Line Graph (Bins)")
        self.lineGraphBinsBranch.setFlags(self.lineGraphBinsBranch.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
        self.lineGraphBinsBranch.setCheckState(0, QtCore.Qt.Unchecked)

    # ---------------------------------------------------------------------------------------------------------------#
    def GraphingGaussianOptionsTree(self):
        # Gaussian Fit Top Branch
        self.gaussianFitTopBranch = QtGui.QTreeWidgetItem()
        self.gaussianFitTopBranch.setText(0, "Gaussian Fit")
        self.gaussianFitTopBranch.setFlags(self.gaussianFitTopBranch.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)

        if self.twoPeakStat == True:
            """Gaussian Fit Children"""
            # Peak One
            self.peakOneBranch = QtGui.QTreeWidgetItem(self.gaussianFitTopBranch)
            self.peakOneBranch.setText(0, "Peak #1")
            self.peakOneBranch.setFlags(self.peakOneBranch.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)

            # Peak Two
            self.peakTwoBranch = QtGui.QTreeWidgetItem(self.gaussianFitTopBranch)
            self.peakTwoBranch.setText(0, "Peak #2")
            self.peakTwoBranch.setFlags(self.peakTwoBranch.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)

            """Peak One Tree Branch Children"""
            # Amplitude Peak One
            self.amplitudePeakOne = QtGui.QTreeWidgetItem(self.peakOneBranch)
            self.amplitudePeakOne.setFlags(self.amplitudePeakOne.flags() | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsTristate)
            self.amplitudePeakOne.setText(0, "Amplitude")
            self.amplitudePeakOne.setCheckState(0, QtCore.Qt.Unchecked)

            # Position Peak One
            self.positionPeakOne = QtGui.QTreeWidgetItem(self.peakOneBranch)
            self.positionPeakOne.setFlags(self.positionPeakOne.flags() | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsTristate)
            self.positionPeakOne.setText(0, "Position")
            self.positionPeakOne.setCheckState(0, QtCore.Qt.Unchecked)

            # Width Peak One
            self.widthPeakOne = QtGui.QTreeWidgetItem(self.peakOneBranch)
            self.widthPeakOne.setFlags(self.widthPeakOne.flags() | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsTristate)
            self.widthPeakOne.setText(0, "Width")
            self.widthPeakOne.setCheckState(0, QtCore.Qt.Unchecked)

            # Amplitude x Width Peak One
            self.ampXWidPeakOne = QtGui.QTreeWidgetItem(self.peakOneBranch)
            self.ampXWidPeakOne.setFlags(self.positionPeakOne.flags() | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsTristate)
            self.ampXWidPeakOne.setText(0, "Amplitude x Width")
            self.ampXWidPeakOne.setCheckState(0, QtCore.Qt.Unchecked)

            """Peak Two Tree Branch Children"""
            # Amplitude Peak Two
            self.amplitudePeakTwo = QtGui.QTreeWidgetItem(self.peakTwoBranch)
            self.amplitudePeakTwo.setFlags(self.amplitudePeakTwo.flags() | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsTristate)
            self.amplitudePeakTwo.setText(0, "Amplitude")
            self.amplitudePeakTwo.setCheckState(0, QtCore.Qt.Unchecked)

            # Position Peak Two
            self.positionPeakTwo = QtGui.QTreeWidgetItem(self.peakTwoBranch)
            self.positionPeakTwo.setFlags(self.positionPeakTwo.flags() | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsTristate)
            self.positionPeakTwo.setText(0, "Position")
            self.positionPeakTwo.setCheckState(0, QtCore.Qt.Unchecked)

            # Width Peak Two
            self.widthPeakTwo = QtGui.QTreeWidgetItem(self.peakTwoBranch)
            self.widthPeakTwo.setFlags(self.widthPeakTwo.flags() | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsTristate)
            self.widthPeakTwo.setText(0, "Width")
            self.widthPeakTwo.setCheckState(0, QtCore.Qt.Unchecked)

            # Amplitude x Width Peak Two
            self.ampXWidPeakTwo = QtGui.QTreeWidgetItem(self.peakTwoBranch)
            self.ampXWidPeakTwo.setFlags(self.ampXWidPeakTwo.flags() | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsTristate)
            self.ampXWidPeakTwo.setText(0, "Amplitude x Width")
            self.ampXWidPeakTwo.setCheckState(0, QtCore.Qt.Unchecked)

        elif self.onePeakStat == True:
            """Children of Gaussian Branch"""
            # Amplitude
            self.onePeakAmplitude = QtGui.QTreeWidgetItem(self.gaussianFitTopBranch)
            self.onePeakAmplitude.setFlags(self.onePeakAmplitude.flags() | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsTristate)
            self.onePeakAmplitude.setText(0, "Amplitude")
            self.onePeakAmplitude.setCheckState(0, QtCore.Qt.Unchecked)

            # Position
            self.onePeakPosition = QtGui.QTreeWidgetItem(self.gaussianFitTopBranch)
            self.onePeakPosition.setFlags(self.onePeakPosition.flags() | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsTristate)
            self.onePeakPosition.setText(0, "Position")
            self.onePeakPosition.setCheckState(0, QtCore.Qt.Unchecked)

            # Width Peak One
            self.onePeakWidth = QtGui.QTreeWidgetItem(self.gaussianFitTopBranch)
            self.onePeakWidth.setFlags(self.onePeakWidth.flags() | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsTristate)
            self.onePeakWidth.setText(0, "Width")
            self.onePeakWidth.setCheckState(0, QtCore.Qt.Unchecked)

            # Amplitude x Width Peak One
            self.onePeakAmpxWid = QtGui.QTreeWidgetItem(self.gaussianFitTopBranch)
            self.onePeakAmpxWid.setFlags(self.onePeakAmpxWid.flags() | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsTristate)
            self.onePeakAmpxWid.setText(0, "Amplitude x Width")
            self.onePeakAmpxWid.setCheckState(0, QtCore.Qt.Unchecked)

        #Adding the top branch to the graphing options tree
        self.graphingOptionsTree.addTopLevelItem(self.gaussianFitTopBranch)
        self.myMainWindow.LFit.setEnabled(True)

    # ---------------------------------------------------------------------------------------------------------------#
    def GraphingLOptionsTree(self):
        if self.LFitStat == False:
            # L Fit Top Branch
            self.LFitTopBranch = QtGui.QTreeWidgetItem()
            self.LFitTopBranch.setText(0, "L Fit")
            self.LFitTopBranch.setFlags(self.LFitTopBranch.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
            """L FitData Children, depending on the peak"""
            if self.onePeakStat == True:
                # RLU Graph
                self.onePeakRLU = QtGui.QTreeWidgetItem(self.LFitTopBranch)
                self.onePeakRLU.setText(0, "RLU")
                self.onePeakRLU.setFlags(self.onePeakRLU.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
                self.onePeakRLU.setCheckState(0, QtCore.Qt.Unchecked)

                # %Change Graph
                self.onePeakRLUPrcChange = QtGui.QTreeWidgetItem(self.LFitTopBranch)
                self.onePeakRLUPrcChange.setText(0, "RLU %-Change")
                self.onePeakRLUPrcChange.setFlags(self.onePeakRLUPrcChange.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
                self.onePeakRLUPrcChange.setCheckState(0, QtCore.Qt.Unchecked)

            elif self.twoPeakStat == True:
                # Peak One
                peakOneBranch = QtGui.QTreeWidgetItem(self.LFitTopBranch)
                peakOneBranch.setText(0, "Peak #1")
                peakOneBranch.setFlags(peakOneBranch.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)

                # Peak Two
                peakTwoBranch = QtGui.QTreeWidgetItem(self.LFitTopBranch)
                peakTwoBranch.setText(0, "Peak #2")
                peakTwoBranch.setFlags(peakTwoBranch.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)

                # RLU Graph Peak one
                self.RLUPeakOne = QtGui.QTreeWidgetItem(peakOneBranch)
                self.RLUPeakOne.setText(0, "RLU")
                self.RLUPeakOne.setFlags(self.RLUPeakOne.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
                self.RLUPeakOne.setCheckState(0, QtCore.Qt.Unchecked)

                # %Change Graph Peak One
                self.RLUPrcChangePeakOne = QtGui.QTreeWidgetItem(peakOneBranch)
                self.RLUPrcChangePeakOne.setText(0, "RLU %-Change")
                self.RLUPrcChangePeakOne.setFlags(self.RLUPrcChangePeakOne.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
                self.RLUPrcChangePeakOne.setCheckState(0, QtCore.Qt.Unchecked)

                # RLU Graph Peak two
                self.RLUPeakTwo = QtGui.QTreeWidgetItem(peakTwoBranch)
                self.RLUPeakTwo.setText(0, "RLU")
                self.RLUPeakTwo.setFlags(self.RLUPeakTwo.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
                self.RLUPeakTwo.setCheckState(0, QtCore.Qt.Unchecked)

                # %Change Graph Peak two
                self.RLUPrcChangePeakTwo = QtGui.QTreeWidgetItem(peakTwoBranch)
                self.RLUPrcChangePeakTwo.setText(0, "RLU %-Change")
                self.RLUPrcChangePeakTwo.setFlags(self.RLUPrcChangePeakTwo.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
                self.RLUPrcChangePeakTwo.setCheckState(0, QtCore.Qt.Unchecked)

            # Adding the top branch to the graphing options tree
            self.graphingOptionsTree.addTopLevelItem(self.LFitTopBranch)
            self.gausFit.doLFit()
            self.LFitStat = True

    # -------------------------------------------------------------------------------------------------------#
    def plottingFits(self):
        """This function calls on the appropriate method to graph for one or two peaks.
        """
        if self.FileError() == False:
            # Raw Data
            if self.colorGraphBranch.checkState(0) == 2:
                self.myMainWindow.PlotColorGraphRawData()
                self.colorGraphBranch.setCheckState(0, 0)
            if self.lineGraphBinsBranch.checkState(0) == 2:
                self.myMainWindow.PlotLineGraphRawDataBins()
                self.lineGraphBinsBranch.setCheckState(0, 0)
            if self.lineGraphLBranch.checkState(0) == 2:
                self.myMainWindow.PlotLineGraphRawDataRLU()
                self.lineGraphLBranch.setCheckState(0, 0)

            if self.onePeakStat == True:
                self.graphingOnePeak()
            elif self.twoPeakStat == True:
                self.graphingTwoPeak()

    # -------------------------------------------------------------------------------------------------------#
    def graphingOnePeak(self):
        if self.onePeakAmplitude.checkState(0) == 2:
            self.gausFit.graphOnePeakAmplitude()
            self.onePeakAmplitude.setCheckState(0, 0)
        if self.onePeakPosition.checkState(0) == 2:
            self.gausFit.graphOnePeakPosition()
            self.onePeakPosition.setCheckState(0, 0)
        if self.onePeakWidth.checkState(0) == 2:
            self.gausFit.graphOnePeakWidth()
            self.onePeakWidth.setCheckState(0, 0)
        if self.onePeakAmpxWid.checkState(0) == 2:
            self.gausFit.graphOnePeakAmplitudeXWidth()
            self.onePeakAmpxWid.setCheckState(0, 0)
        if self.LFitStat == True:
            if self.onePeakRLU.checkState(0) == 2:
                self.gausFit.graphOnePeakLFitPos()
                self.onePeakRLU.setCheckState(0, 0)
            if self.onePeakRLUPrcChange.checkState(0) == 2:
                self.gausFit.percentageChangeLConstantOnePeak()
                self.onePeakRLUPrcChange.setCheckState(0, 0)

    # -------------------------------------------------------------------------------------------------------#
    def graphingTwoPeak(self):
        # Peak One
        if self.amplitudePeakOne.checkState(0) == 2:
            self.gausFit.graphTwoPeakAmplitude1()
            self.amplitudePeakOne.setCheckState(0, 0)
        if self.positionPeakOne.checkState(0) == 2:
            self.gausFit.graphTwoPeakPosition1()
            self.positionPeakOne.setCheckState(0, 0)
        if self.widthPeakOne.checkState(0) == 2:
            self.gausFit.graphTwoPeakWidth1()
            self.widthPeakOne.setCheckState(0, 0)
        if self.ampXWidPeakOne.checkState(0) == 2:
            self.gausFit.graphTwoPeakAmplitudeXWidth1()
            self.ampXWidPeakOne.setCheckState(0, 0)

        # Peak Two
        if self.amplitudePeakTwo.checkState(0) == 2:
            self.gausFit.graphTwoPeakAmplitude2()
            self.amplitudePeakTwo.setCheckState(0, 0)
        if self.positionPeakTwo.checkState(0) == 2:
            self.gausFit.graphTwoPeakPosition2()
            self.positionPeakTwo.setCheckState(0, 0)
        if self.widthPeakTwo.checkState(0) == 2:
            self.gausFit.graphTwoPeakWidth2()
            self.widthPeakTwo.setCheckState(0, 0)
        if self.ampXWidPeakTwo.checkState(0) == 2:
            self.gausFit.graphTwoPeakAmplitudeXWidth2()
            self.ampXWidPeakTwo.setCheckState(0, 0)
        if self.LFitStat == True:
            if self.RLUPeakOne.checkState(0) == 2:
                self.gausFit.graphTwoPeakLFitPos1()
                self.RLUPeakOne.setCheckState(0, 0)
            if self.RLUPrcChangePeakOne.checkState(0) == 2:
                self.gausFit.percentageChangeLConstantPeakOne()
                self.RLUPrcChangePeakOne.setCheckState(0, 0)
            if self.RLUPeakTwo.checkState(0) == 2:
                self.gausFit.graphTwoPeakLFitPos2()
                self.RLUPeakTwo.setCheckState(0, 0)
            if self.RLUPrcChangePeakTwo.checkState(0) == 2:
                self.gausFit.percentageChangeLConstantPeakTwo()
                self.RLUPrcChangePeakTwo.setCheckState(0, 0)



