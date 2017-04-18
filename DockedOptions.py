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
        self.dockGaussianFitOptions

 # -----------------------------------------------------------------------------#
    def dockGaussianFitOptions(self):
        """Function that creates the dockWidget, Graph Options for fitting one
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

        FileHLayout.addWidget(self.fileNameLabel)
        FileHLayout.addWidget(self.rdOnlyFileNameG)
        FileHLayout.addStretch(1)

        BtnLayout.addStretch(1)
        BtnLayout.addWidget(self.GraphFittingOneBtn)

        layout.addRow(FileHLayout)
        layout.addRow(self.graphCheckBx)
        layout.addRow(BtnLayout)
        self.dataDocked.setLayout(layout)
        self.dockDataGausFit.setWidget(self.dataDocked)

        # Adding the docked widget to the main window
        self.myMainWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.dockDataGausFit)
        self.myMainWindow.tabifyDockWidget(self.dockRawData, self.dockDataGausFit)


    def GraphFittingOneCheckBox(self):
        """This function contains a group box with check boxes for fitting one"""
        self.graphCheckBx = QtGui.QGroupBox("Select Graphs")

        self.checkBxAmplitude = QtGui.QCheckBox("Amplitude")
        self.checkBxPeakPosition = QtGui.QCheckBox("Peak position")
        self.checkBxPeakWidth = QtGui.QCheckBox("Peak width")
        self.checkBxAmplitudeXWidth = QtGui.QCheckBox("Amplitude x Width")
        self.checkBxGraphAll = QtGui.QCheckBox("Graph all")

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.checkBxAmplitude)
        vbox.addWidget(self.checkBxPeakPosition)
        vbox.addWidget(self.checkBxPeakWidth)
        vbox.addWidget(self.checkBxAmplitudeXWidth)
        vbox.addWidget(self.checkBxGraphAll)

        self.checkBxAmplitude.stateChanged.connect(self.CheckFittingOneCheckBoxes)
        self.checkBxAmplitudeXWidth.stateChanged.connect(self.CheckFittingOneCheckBoxes)
        self.checkBxPeakWidth.stateChanged.connect(self.CheckFittingOneCheckBoxes)
        self.checkBxPeakPosition.stateChanged.connect(self.CheckFittingOneCheckBoxes)
        self.checkBxGraphAll.stateChanged.connect(self.CheckFittingOneCheckBoxes)

        self.graphCheckBx.setLayout(vbox)

    # ----------------------------------------------------------------------------------------------------------#
    def restoreDockGaussianFitOptions(self):
        """This funtion restores the Graphing Options Dock Widget for Fitting One, if it's close"""
        if (self.dockDataGausFit.isVisible() == False):
            self.dockGaussianFitOptions()
            if self.fileName is not "" and self.fileName is not None:
                self.rdOnlyFileNameG.setText(self.fileName)
                self.rdOnlyFileNameG.setStatusTip(self.fileName)

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

                if self.checkBxAmplitude.isChecked() and self.checkBxGraphAll.isChecked() == False:
                    self.gausFit.graphAmplitude()

                if self.checkBxPeakPosition.isChecked() and self.checkBxGraphAll.isChecked() == False:
                    self.gausFit.graphPeakPosition()

                if self.checkBxPeakWidth.isChecked() and self.checkBxGraphAll.isChecked() == False:
                    self.gausFit.graphPeakWidth()

                if self.checkBxAmplitudeXWidth.isChecked() and self.checkBxGraphAll.isChecked() == False:
                    self.gausFit.graphAmplitudeXWidth()

                if self.checkBxGraphAll.isChecked():
                    self.gausFit.graphAll()

        self.checkBxGraphAll.setCheckState(QtCore.Qt.Unchecked)
        self.checkBxAmplitude.setCheckState(QtCore.Qt.Unchecked)
        self.checkBxAmplitudeXWidth.setCheckState(QtCore.Qt.Unchecked)
        self.checkBxPeakPosition.setCheckState(QtCore.Qt.Unchecked)
        self.checkBxPeakWidth.setCheckState(QtCore.Qt.Unchecked)

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
        if self.fileName is " " or self.fileName == None:
            QtGui.QMessageBox.warning(self, "Error - No File", "There is no data to fit."
                                                               " Make sure a file has been open.")
        else:
            if os.path.isfile(self.fileName) == False:
                QtGui.QMessageBox.warning(self, "Error - No File", "There is no data to fit."
                                                                   " Make sure a file has been open.")
            else:
                if (self.gausFitStat == True):
                    self.restoreDockGaussianFitOptions()
                else:
                    chosePeak = self.PeakDialog()
                    if (chosePeak == 'One'):
                        self.gausFit.OnePeakFitting(self.fileName)
                        self.dockGaussianFitOptions()
                        self.gausFitStat = True
                    elif (chosePeak == 'Two'):
                        self.gausFit.gausInputDialog()
                        self.gausFitStat = True


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

        filters = "Text files (*.txt);;Python files (*.py)"
        selectedFilter = "Any file (*.*);;Text files (*.txt);;Python files (*.py)"
        self.fileName = QtGui.QFileDialog.getOpenFileName(self, "Open File")

        self.rdOnlyFileName.setText(self.fileName)
        self.rdOnlyFileName.setStatusTip(self.fileName)
        self.gausFitStat = False

    # ------------------------------------------------------------------------------------#
    def GraphFittingOneButton(self):
        """Funtion that creates a graph button, connects to the GraphDataFittingOne() method"""
        self.GraphFittingOneBtn = QtGui.QPushButton('Graph', self)
        self.GraphFittingOneBtn.setStatusTip("Graphs the check graphs")
        self.GraphFittingOneBtn.clicked.connect(self.GraphDataGausFit)


    def BrowseButton(self):
        """Function that creates a browse method, connects to the openFile() method"""
        # Button next to the FileNameRdOnly label and LineEdit
        self.BrowseBtn = QtGui.QPushButton('Browse', self)
        self.BrowseBtn.clicked.connect(self.openFile)
        self.BrowseBtn.setStatusTip("Browse and open an existing file")

    def GraphRawDataButton(self):
        """Function that creates a graph button, connects to the GraphData() method"""
        self.GraphRawDataBtn = QtGui.QPushButton('Graph', self)
        self.GraphRawDataBtn.setStatusTip("Graphs the check graphs")
        self.GraphRawDataBtn.clicked.connect(self.GraphRawData)

    # ------------------------------------------------------------------------------------#
    def CheckFittingOneCheckBoxes(self):
        """This function contains different conditions for the check boxes in data tab"""
        # Checks Graph all and unchecks the rest, if all are selected
        if self.checkBxGraphAll.isChecked() is False and self.checkBxPeakPosition.isEnabled() is False \
                and self.checkBxAmplitude.isEnabled() is False and self.checkBxPeakWidth.isEnabled() is False \
                and self.checkBxAmplitudeXWidth.isEnabled() is False:
            self.checkBxPeakPosition.setCheckState(QtCore.Qt.Unchecked)
            self.checkBxAmplitude.setCheckState(QtCore.Qt.Unchecked)
            self.checkBxPeakWidth.setCheckState(QtCore.Qt.Unchecked)
            self.checkBxAmplitudeXWidth.setCheckState(QtCore.Qt.Unchecked)
            self.checkBxPeakPosition.setEnabled(True)
            self.checkBxAmplitude.setEnabled(True)
            self.checkBxPeakWidth.setEnabled(True)
            self.checkBxAmplitudeXWidth.setEnabled(True)

        # Checks and disables other boxes when Graph all is checked
        if self.checkBxGraphAll.isChecked():
            self.checkBxPeakPosition.setCheckState(QtCore.Qt.Checked)
            self.checkBxAmplitude.setCheckState(QtCore.Qt.Checked)
            self.checkBxPeakWidth.setCheckState(QtCore.Qt.Checked)
            self.checkBxAmplitudeXWidth.setCheckState(QtCore.Qt.Checked)
            self.checkBxPeakPosition.setEnabled(False)
            self.checkBxAmplitude.setEnabled(False)
            self.checkBxPeakWidth.setEnabled(False)
            self.checkBxAmplitudeXWidth.setEnabled(False)

        # Checks Graph all if all other boxes are checked
        if self.checkBxAmplitude.isChecked() and self.checkBxPeakPosition.isChecked() \
                and self.checkBxPeakWidth.isChecked() and self.checkBxAmplitudeXWidth.isChecked():
            self.checkBxGraphAll.setChecked(True)

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

    def GraphRawDataCheckBox(self):
        """This function contains a group box with check boxes for fitting one"""
        self.graphCheckBx = QtGui.QGroupBox("Select Graphs")

        self.checkBxColorGraph = QtGui.QCheckBox("Color Graph")
        self.checkBxLineGraph = QtGui.QCheckBox("Line Graph")

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.checkBxColorGraph)
        vbox.addWidget(self.checkBxLineGraph)

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

                if self.checkBxLineGraph.isChecked():
                    self.myMainWindow.PlotLineGraphRawData()

        self.checkBxColorGraph.setCheckState(QtCore.Qt.Unchecked)
        self.checkBxLineGraph.setCheckState(QtCore.Qt.Unchecked)


