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


class DockedOption(QtGui.QDockWidget):

    def __init__ (self, parent=None):
        super(DockedOption, self).__init__(parent)
        self.fileName = None
        self.myMainWindow = parent
        self.gausFit = GaussianFitting(self)

        self.gausFitStat = False
        self.LFitStat = False

        self.onePeakGausFitStat = False
        self.onePeakLFit = False
        self.twoPeakGausFitStat = False
        self.twoPeakLFitStat = False


        self.TT = [0][0] # 2D array where raw data is stored

    # -----------------------------------------------------------------------------#
    def dockOnePeakGaussianFitOptions(self):  # Beginning of one peak gaussian fit
        """Function that creates the dockWidget, Graph Options for Gaussian fit with one Peak
        """
        self.dockOnePeakFits = QtGui.QDockWidget("Fit", self)
        self.dockOnePeakFits.setFloating(False)
        self.dockOnePeakFits.setMaximumWidth(320)
        self.dockOnePeakFits.setMinimumWidth(320)
        self.dockOnePeakFits.setAllowedAreas(QtCore.Qt.RightDockWidgetArea | QtCore.Qt.LeftDockWidgetArea)

        layout = QtGui.QFormLayout()
        FileHLayout = QtGui.QHBoxLayout()
        BtnLayout = QtGui.QHBoxLayout()
        dataDocked = QtGui.QWidget()

        self.FileNameRdOnlyBox()
        self.GraphOnePeakGaussianFitCheckBoxes()
        self.GraphOnePeakFitsButton()

        FileHLayout.addWidget(self.fileNameLabel)
        FileHLayout.addWidget(self.rdOnlyFileNameG)
        FileHLayout.addStretch(1)

        BtnLayout.addStretch(1)
        BtnLayout.addWidget(self.GraphOnePeakFitsBtn)

        layout.addRow(FileHLayout)
        layout.addRow(self.graphPeakOneGausFitCheckBx)

        if self.onePeakLFit == True:
            layout.addRow(self.graphLCheckBx)

        layout.addRow(BtnLayout)
        dataDocked.setLayout(layout)
        self.dockOnePeakFits.setWidget(dataDocked)

        # Adding the docked widget to the main window
        self.myMainWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.dockOnePeakFits)
        self.myMainWindow.tabifyDockWidget(self.dockRawData, self.dockOnePeakFits)

    def GraphOnePeakGaussianFitCheckBoxes(self):
        """This function contains a group box with check boxes for Gaussian fit with one peak"""
        self.graphPeakOneGausFitCheckBx = QtGui.QGroupBox("Gaussian")

        self.checkBxOnePeakAmplitude = QtGui.QCheckBox("Amplitude")
        self.checkBxOnePeakPosition = QtGui.QCheckBox("Position")
        self.checkBxOnePeakWidth = QtGui.QCheckBox("Width")
        self.checkBxOnePeakAmplitudeXWidth = QtGui.QCheckBox("Amplitude x Width")

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.checkBxOnePeakAmplitude)
        vbox.addWidget(self.checkBxOnePeakPosition)
        vbox.addWidget(self.checkBxOnePeakWidth)
        vbox.addWidget(self.checkBxOnePeakAmplitudeXWidth)
        self.graphPeakOneGausFitCheckBx.setLayout(vbox)

        if self.onePeakLFit == True:
            self.graphLCheckBx = QtGui.QGroupBox("L")
            self.checkBxOnePeakLPosGraph = QtGui.QCheckBox("Position")
            vboxL = QtGui.QVBoxLayout()
            vboxL.addWidget(self.checkBxOnePeakLPosGraph)
            self.graphLCheckBx.setLayout(vboxL)


    def GraphOnePeakFits(self):
        """This function checks which checkboxes are checked and then calls on the appropriate
        function to graph the desired fitted data. (One Peak Gaussian Fit)
        """
        if self.checkBxOnePeakAmplitude.isChecked():
            self.gausFit.graphOnePeakAmplitude()
            self.checkBxOnePeakAmplitude.setCheckState(QtCore.Qt.Unchecked)

        if self.checkBxOnePeakPosition.isChecked():
            self.checkBxOnePeakPosition.setCheckState(QtCore.Qt.Unchecked)
            self.gausFit.graphOnePeakPosition()

        if self.checkBxOnePeakWidth.isChecked():
            self.checkBxOnePeakWidth.setCheckState(QtCore.Qt.Unchecked)
            self.gausFit.graphOnePeakWidth()

        if self.checkBxOnePeakAmplitudeXWidth.isChecked():
            self.gausFit.graphOnePeakAmplitudeXWidth()
            self.checkBxOnePeakAmplitudeXWidth.setCheckState(QtCore.Qt.Unchecked)

        if self.onePeakLFit == True:
            if self.checkBxOnePeakLPosGraph.isChecked():
                self.gausFit.graphOnePeakLFitPos()
                self.checkBxOnePeakLPosGraph.setCheckState(QtCore.Qt.Unchecked)

    # -----------------------------------------------------------------------------#
    def dockTwoPeakGaussianFitOptions(self):
        """Function that creates the dockWidget Gaussian fit options for two peaks.
        """
        self.dockDataGausFit = QtGui.QDockWidget("Gaussian Fit", self)
        self.dockDataGausFit.setFloating(False)
        self.dockDataGausFit.setMaximumWidth(320)
        self.dockDataGausFit.setMinimumWidth(320)
        self.dockDataGausFit.setAllowedAreas(QtCore.Qt.RightDockWidgetArea | QtCore.Qt.LeftDockWidgetArea)

        layout = QtGui.QFormLayout()
        FileHLayout = QtGui.QHBoxLayout()
        BtnLayout = QtGui.QHBoxLayout()
        self.dataDocked = QtGui.QWidget()

        self.FileNameRdOnlyBox()
        self.GraphFittingOneCheckBox()
        self.GraphFittingOneButton()
        self.GraphAllButton()

        FileHLayout.addWidget(self.fileNameLabel)
        FileHLayout.addWidget(self.rdOnlyFileNameG)
        FileHLayout.addStretch(1)

        BtnLayout.addWidget(self.GraphAllBtn)
        BtnLayout.addStretch(1)
        BtnLayout.addWidget(self.GraphFittingOneBtn)

        layout.addRow(FileHLayout)
        layout.addRow(self.graphCheckBx1)
        layout.addRow(self.graphCheckBx2)
        layout.addRow(BtnLayout)
        self.dataDocked.setLayout(layout)
        self.dockDataGausFit.setWidget(self.dataDocked)

        # Adding the docked widget to the main window
        self.myMainWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.dockDataGausFit)
        self.myMainWindow.tabifyDockWidget(self.dockRawData, self.dockDataGausFit)


    def GraphFittingOneCheckBox(self):
        """This function contains a group box with check boxes for fitting one"""
        self.graphCheckBx1 = QtGui.QGroupBox("Peak #1")
        self.graphCheckBx2 = QtGui.QGroupBox("Peak #2")

        self.checkBxAmplitude1 = QtGui.QCheckBox("Amplitude")
        self.checkBxPeakPosition1 = QtGui.QCheckBox("Position")
        self.checkBxPeakWidth1 = QtGui.QCheckBox("Width")
        self.checkBxAmplitudeXWidth1 = QtGui.QCheckBox("Amplitude x Width")
        self.checkBxAmplitude2 = QtGui.QCheckBox("Amplitude")
        self.checkBxPeakPosition2 = QtGui.QCheckBox("Position")
        self.checkBxPeakWidth2 = QtGui.QCheckBox("Width")
        self.checkBxAmplitudeXWidth2  = QtGui.QCheckBox("Amplitude x Width")
        self.checkBxGraphAll = QtGui.QCheckBox("Graph all")

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.checkBxAmplitude1)
        vbox.addWidget(self.checkBxPeakPosition1)
        vbox.addWidget(self.checkBxPeakWidth1)
        vbox.addWidget(self.checkBxAmplitudeXWidth1)

        vbox2 = QtGui.QVBoxLayout()
        vbox2.addWidget(self.checkBxAmplitude2)
        vbox2.addWidget(self.checkBxPeakPosition2)
        vbox2.addWidget(self.checkBxPeakWidth2)
        vbox2.addWidget(self.checkBxAmplitudeXWidth2)

        self.graphCheckBx1.setLayout(vbox)
        self.graphCheckBx2.setLayout(vbox2)

    # -----------------------------------------------------------------------------------------#
    def GraphDataGausFit(self):
        """Function that graphs the information from the file and calls on the different methods to graph
        depending on the check boxes the user has chosen. Checks for the fileName not to be empty and
        the path to lead to an actual file. This method is called in the Graphing Utilities file
        """

        if self.fileName is "" or self.fileName is None:
            QtGui.QMessageBox.warning(self, "Error - No File", "There is no data to graph."
                                                               " Make sure a file has been open.")
        else:
            if os.path.isfile(self.fileName) == False:
                QtGui.QMessageBox.warning(self, "Error - No File", "There is no data to graph."
                                                                   " Make sure a file has been open.")
            else:

                if self.checkBxAmplitude1.isChecked():
                    self.gausFit.graphAmplitude1()

                if self.checkBxPeakPosition1.isChecked():
                    self.gausFit.graphPeakPosition1()

                if self.checkBxPeakWidth1.isChecked():
                    self.gausFit.graphPeakWidth1()

                if self.checkBxAmplitudeXWidth1.isChecked():
                    self.gausFit.graphAmplitudeXWidth1()

                if self.checkBxAmplitude2.isChecked():
                    self.gausFit.graphAmplitude2()

                if self.checkBxPeakPosition2.isChecked():
                    self.gausFit.graphPeakPosition2()

                if self.checkBxPeakWidth2.isChecked():
                    self.gausFit.graphPeakWidth2()

                if self.checkBxAmplitudeXWidth2.isChecked():
                    self.gausFit.graphAmplitudeXWidth2()

        self.checkBxAmplitude1.setCheckState(QtCore.Qt.Unchecked)
        self.checkBxAmplitudeXWidth1.setCheckState(QtCore.Qt.Unchecked)
        self.checkBxPeakPosition1.setCheckState(QtCore.Qt.Unchecked)
        self.checkBxPeakWidth1.setCheckState(QtCore.Qt.Unchecked)
        self.checkBxAmplitude2.setCheckState(QtCore.Qt.Unchecked)
        self.checkBxAmplitudeXWidth2.setCheckState(QtCore.Qt.Unchecked)
        self.checkBxPeakPosition2.setCheckState(QtCore.Qt.Unchecked)
        self.checkBxPeakWidth2.setCheckState(QtCore.Qt.Unchecked)

    # ----------------------------------------------------------------------------------------------------------#
    def restoreDockGaussianFitOptions(self):
        """This funtion restores the Graphing Options Dock Widget for the Gaussian fit. It checks which Peak to
        restore, either one peak or two. It only restores them if they are not visible."""
        if self.onePeakGausFitStat == True:
            if (self.dockOnePeakFits.isVisible() == False):
                self.dockOnePeakGaussianFitOptions()
        elif self.twoPeakGausFitStat == True:
            if (self.dockDataGausFit.isVisible() == False):
                self.dockTwoPeakGaussianFitOptions()

        if self.fileName is not "" and self.fileName is not None:
            self.rdOnlyFileNameG.setText(self.fileName)
            self.rdOnlyFileNameG.setStatusTip(self.fileName)

    # ------------------------------------------------------------------------------------#
    def FileNameRdOnlyBox(self):
        """This method contains a QLineEdit and label that display the selected file
            next to the browse button"""
        self.rdOnlyFileName = QtGui.QLineEdit()
        self.rdOnlyFileName.setReadOnly(True)
        self.rdOnlyFileName.setTextMargins(0, 0, 10, 0)
        self.rdOnlyFileName.setFixedWidth(125)

        #For the Gaussioan Fit
        self.rdOnlyFileNameG = QtGui.QLineEdit()
        self.rdOnlyFileNameG.setReadOnly(True)
        self.rdOnlyFileNameG.setTextMargins(0, 0, 10, 0)
        self.rdOnlyFileNameG.setFixedWidth(200)

        # Label
        self.fileNameLabel = QtGui.QLabel()
        self.fileNameLabel.setText("File Name:")

    # ------------------------------------------------------------------------------------#
    def GaussianFittingData(self):
        if (self.gausFitStat == True):
            self.restoreDockGaussianFitOptions()
        else:
            chosePeak = self.PeakDialog()
            if (chosePeak == 'One'):
                self.gausFit.gausOnePeakInputDialog()
            elif (chosePeak == 'Two'):
                self.gausFit.gausTwoPeakInputDialog()


    def PeakDialog(self):
        """Method that asks the user to import """
        peakList = ['One', 'Two']
        text, ok = QtGui.QInputDialog.getItem(self, 'Peak Fit', 'Choose Peak: ', peakList)

        if ok:
            return text

    # ------------------------------------------------------------------------------------#
    def openFile(self):
        """This method opens the file """
        #Sets the fileName rdOnlyBox to blank, if they try to open another file
        self.rdOnlyFileName.setText(" ")
        self.rdOnlyFileName.setStatusTip(" ")
        self.rdOnlyFileNameG.setText(" ")
        self.rdOnlyFileNameG.setStatusTip(" ")

        filters = "Text files (*.txt);;Python files (*.py)"
        selectedFilter = "Any file (*.*);;Text files (*.txt);;Python files (*.py)"
        self.fileName = QtGui.QFileDialog.getOpenFileName(self, "Open File")

        self.rdOnlyFileName.setText(self.fileName)
        self.rdOnlyFileName.setStatusTip(self.fileName)
        self.gausFitStat = False
        self.LFitStat = False
        self.onePeakGausFitStat = False
        self.gausFit.continueGraphingEachFit = True
        if (self.rdOnlyFileName.text() != ""):
            self.gausFit.LInputDialog()

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
    def GraphFittingOneButton(self):
        """Funtion that creates a graph button, connects to the GraphDataFittingOne() method"""
        self.GraphFittingOneBtn = QtGui.QPushButton('Graph', self)
        self.GraphFittingOneBtn.setStatusTip("Graphs the checked graphs")
        self.GraphFittingOneBtn.clicked.connect(self.GraphDataGausFit)

    def GraphOnePeakFitsButton(self):
        """Funtion that creates a graph button, connects to the GraphDataFittingOne() method"""
        self.GraphOnePeakFitsBtn = QtGui.QPushButton('Graph', self)
        self.GraphOnePeakFitsBtn.setStatusTip("Graphs the checked graphs")
        self.GraphOnePeakFitsBtn.clicked.connect(self.GraphOnePeakFits)

    def BrowseButton(self):
        """Function that creates a browse method, connects to the openFile() method"""
        # Button next to the FileNameRdOnly label and LineEdit
        self.BrowseBtn = QtGui.QPushButton('Browse', self)
        self.BrowseBtn.clicked.connect(self.openFile)
        self.BrowseBtn.setStatusTip("Browse and open an existing file")

    def GraphRawDataButton(self):
        """Function that creates a graph button, connects to the GraphData() method"""
        self.GraphRawDataBtn = QtGui.QPushButton('Graph', self)
        self.GraphRawDataBtn.setStatusTip("Graphs the checked boxes")
        self.GraphRawDataBtn.clicked.connect(self.GraphRawData)

    def GraphAllButton(self):
        """Function that creates a graph button, the connects to the method that graphs all the graphs"""
        self.GraphAllBtn = QtGui.QPushButton('Graph all', self)
        self.GraphAllBtn.setStatusTip("Graphs all the fitted data graphs")
        self.GraphAllBtn.clicked.connect(self.gausFit.graphAll)

    def GraphLFitButton(self):
        """Function that creates a graph button, connects to the GraphLFit()"""
        self.GraphLFitBtn = QtGui.QPushButton('Graph', self)
        self.GraphLFitBtn.setStatusTip("Graphs the selected L Fit check boxes")
        self.GraphLFitBtn.clicked.connect(self.GraphLFit)

    # --------------------------------------------------------------------------------------------#
    def DockRawDataOptions(self):
        """Function that creates the dockWidget, Graph Options for fitting one
        """
        self.dockRawData = QtGui.QDockWidget("Raw Data", self)
        self.dockRawData.setFloating(False)
        self.dockRawData.setMaximumWidth(320)
        self.dockRawData.setMinimumWidth(320)
        self.dockRawData.setAllowedAreas(QtCore.Qt.RightDockWidgetArea | QtCore.Qt.LeftDockWidgetArea)

        layout = QtGui.QFormLayout()
        FileHLayout = QtGui.QHBoxLayout()
        BtnLayout = QtGui.QHBoxLayout()
        self.dataDockedWidget = QtGui.QWidget()

        self.FileNameRdOnlyBox()
        self.BrowseButton()
        self.GraphRawDataButton()
        self.GraphRawDataCheckBox()

        FileHLayout.addWidget(self.fileNameLabel)
        FileHLayout.addWidget(self.rdOnlyFileName)
        FileHLayout.addStretch(1)
        FileHLayout.addWidget(self.BrowseBtn)

        BtnLayout.addStretch(1)
        BtnLayout.addWidget(self.GraphRawDataBtn)

        layout.addRow(FileHLayout)
        layout.addRow(self.graphCheckBx)
        layout.addRow(BtnLayout)
        self.dataDockedWidget.setLayout(layout)
        self.dockRawData.setWidget(self.dataDockedWidget)

        # Adding the docked widget to the main window
        self.myMainWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.dockRawData)
        # Checks to see if the Raw data is being restored when the fitted options have been displayed
        if (self.onePeakGausFitStat == True):
                if self.dockOnePeakFits.isVisible():
                        self.myMainWindow.tabifyDockWidget(self.dockRawData, self.dockOnePeakFits)
        elif self.twoPeakGausFitStat == True:
            if self.twoPeakLFitStat == True:
                if self.twoPeakDockLFit.isVisible() == True:
                    self.myMainWindow.tabifyDockWidget(self.dockRawData, self.dockDataGausFit)
                    self.myMainWindow.tabifyDockWidget(self.dockDataGausFit, self.twoPeakDockLFit)
                else:
                    self.myMainWindow.tabifyDockWidget(self.dockRawData, self.dockOnePeakGaussianFitOptions)
            else:
                self.myMainWindow.tabifyDockWidget(self.dockRawData, self.dockOnePeakGaussianFitOptions)


    def GraphRawDataCheckBox(self):
        """This function contains a group box with check boxes for fitting one"""
        self.graphCheckBx = QtGui.QGroupBox("Select Graphs")

        self.checkBxColorGraph = QtGui.QCheckBox("Color Graph")
        self.checkBxLineGraphRLU = QtGui.QCheckBox("Line Graph (RLU)")
        self.checkBxLineGraphBins = QtGui.QCheckBox("Line Graph (Bins)")

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.checkBxColorGraph)
        vbox.addWidget(self.checkBxLineGraphRLU)
        vbox.addWidget(self.checkBxLineGraphBins)

        self.graphCheckBx.setLayout(vbox)

    # ----------------------------------------------------------------------------------------------------------#
    def restoreRawDataOptions(self):
        """This funtion restores the Graphing Options Dock Widget for Fitting One, if it's closed """
        if self.dockRawData.isVisible() == False:
            self.DockRawDataOptions()
            if self.fileName is not "" and self.fileName is not None:
                self.rdOnlyFileName.setText(self.fileName)
                self.rdOnlyFileName.setStatusTip(self.fileName)

    # ----------------------------------------------------------------------------------------------------------#
    def GraphRawData(self):
        """Function that depending on the check boxes the user has chosen it plots the raw data."""

        self.myMainWindow.fileNm = self.fileName
        if self.fileName is "" or self.fileName is None:
            QtGui.QMessageBox.warning(self, "Error - No File", "There is no data to graph."
                                                               " Make sure a file has been open.")
        else:
            if os.path.isfile(self.fileName) == False:
                QtGui.QMessageBox.warning(self, "Error - No File", "There is no data to graph."
                                                                   " Make sure a file has been open.")
            else:
                if self.checkBxColorGraph.isChecked():
                    self.myMainWindow.PlotColorGraphRawData()

                if self.checkBxLineGraphRLU.isChecked():
                    self.myMainWindow.PlotLineGraphRawDataRLU()

                if self.checkBxLineGraphBins.isChecked():
                    self.myMainWindow.PlotLineGraphRawDataBins()

        self.checkBxColorGraph.setCheckState(QtCore.Qt.Unchecked)
        self.checkBxLineGraphRLU.setCheckState(QtCore.Qt.Unchecked)
        self.checkBxLineGraphBins.setCheckState(QtCore.Qt.Unchecked)

    # ----------------------------------------------------------------------------------------------------------#
    def DockLFitOptions(self):
        """Function that creates the dockWidget, Graph Options for fitting one
        """
        self.twoPeakDockLFit = QtGui.QDockWidget("L Fit", self)
        self.twoPeakDockLFit.setFloating(False)
        self.twoPeakDockLFit.setMaximumWidth(320)
        self.twoPeakDockLFit.setMinimumWidth(320)
        self.twoPeakDockLFit.setAllowedAreas(QtCore.Qt.RightDockWidgetArea | QtCore.Qt.LeftDockWidgetArea)

        layout = QtGui.QFormLayout()
        FileHLayout = QtGui.QHBoxLayout()
        BtnLayout = QtGui.QHBoxLayout()
        self.dataDockedWidget = QtGui.QWidget()

        self.FileNameRdOnlyBox()
        self.GraphLFitButton()
        self.GraphLFitCheckBox()

        FileHLayout.addWidget(self.fileNameLabel)
        FileHLayout.addWidget(self.rdOnlyFileNameG)
        FileHLayout.addStretch(1)

        BtnLayout.addStretch(1)
        BtnLayout.addWidget(self.GraphLFitBtn)

        layout.addRow(FileHLayout)
        layout.addRow(self.graphLCheckBx)
        layout.addRow(BtnLayout)
        self.dataDockedWidget.setLayout(layout)
        self.twoPeakDockLFit.setWidget(self.dataDockedWidget)

        # Adding the docked widget to the main window
        self.myMainWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.twoPeakDockLFit)

        if (self.dockDataGausFit.isVisible() == True):
            self.myMainWindow.tabifyDockWidget(self.dockDataGausFit, self.twoPeakDockLFit)
        elif (self.dockRawData.isVisible() == True):
            self.myMainWindow.tabifyDockWidget(self.dockRawData, self.twoPeakDockLFit)

    def GraphLFitCheckBox(self):
        """This function contains a group box with check boxes for fitting one"""
        self.graphLCheckBx = QtGui.QGroupBox("Select Graphs")

        self.checkBxLPos1Graph = QtGui.QCheckBox("Position #1")
        self.checkBxLPos2Graph = QtGui.QCheckBox("Position #2")

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.checkBxLPos1Graph)
        vbox.addWidget(self.checkBxLPos2Graph)

        self.graphLCheckBx.setLayout(vbox)

    # ----------------------------------------------------------------------------------------------------------#
    def restoreLFitOptions(self):
        """This funtion restores the Graphing Options Dock Widget for Fitting One, if it's closed """
        if  self.onePeakLFit == True:
            self.restoreOnePeakLFit()
        elif self.dockLFit.isVisible() == False:
            self.restoreTwoPeakLFit()

        # Sets the title of the rdOnlyFileNameG
        if self.fileName is not "" and self.fileName is not None:
            self.rdOnlyFileNameG.setText(self.fileName)
            self.rdOnlyFileNameG.setStatusTip(self.fileName)

    # ------------------------------------------------------------------------------------#
    def restoreOnePeakLFit(self):
        if self.dockOnePeakFits.isVisible() == False:
            self.dockOnePeakGaussianFitOptions()

    # ------------------------------------------------------------------------------------#
    def restoreTwoPeakLFit(self):
        if self.twoPeakDockLFit .isVisible() == False:
            self.DockLFitOptions()

    # ----------------------------------------------------------------------------------------------------------#
    def GraphLFit(self):
        """Function that depending on the check boxes the user has chosen it plots the raw data."""
        if self.checkBxLPos1Graph.isChecked():
            self.gausFit.graphLFitPos1()

        if self.checkBxLPos2Graph.isChecked():
            self.gausFit.graphLFitPos2()

        self.checkBxLPos1Graph.setCheckState(QtCore.Qt.Unchecked)
        self.checkBxLPos2Graph.setCheckState(QtCore.Qt.Unchecked)

    # ------------------------------------------------------------------------------------#
    def LFittingData(self):
        """This function either restores or initializes the L Fit Docked Options
        """
        if (self.LFitStat == True):
            self.restoreLFitOptions()
        else:
            self.gausFit.doLFit()

