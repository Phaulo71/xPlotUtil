#!/usr/bin/env python

"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.
"""
# --------------------------------------------------------------------------------------#
from __future__ import unicode_literals
import sys
import os
import numpy as np
from pylab import *
from matplotlib.backends import qt_compat


use_pyside = qt_compat.QT_API == qt_compat.QT_API_PYSIDE
if use_pyside:
    from PySide import QtGui, QtCore
else:
    from PyQt4 import QtGui, QtCore

import matplotlib.pyplot as plt
matplotlib.use('Qt4Agg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar
import gc
# --------------------------------------------------------------------------------------#

class MainWindow (QtGui.QMainWindow):

    def __init__ (self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setGeometry(50, 50, 800, 700)
        self.setMinimumSize(800, 700)
        self.setWindowTitle("xPlot Util")
        self.setWindowIcon(QtGui.QIcon('Icons/Graph.png'))
        self.fileName = None
        self.canvasArray = []
        self.figArray = []

        self.SetupComponents()
        self.windowTabs()
        self.dockFittingOptionOne()
        self.CheckGraphCheckBoxes()
        self.setCentralWidget(self.tabWidget)

    # -----------------------------------------------------------------------------#
    def dockFittingOptionOne(self):
        """Function that creates the dockWidget, Graph Options for fitting one"""

        self.dockDataGraphing = QtGui.QDockWidget("xPlotting Options", self)
        self.dockDataGraphing.setFloating(False)
        self.dockDataGraphing.setMaximumWidth(325)
        self.dockDataGraphing.setAllowedAreas(QtCore.Qt.RightDockWidgetArea | QtCore.Qt.LeftDockWidgetArea)

        layout = QtGui.QFormLayout()
        FileHLayout = QtGui.QHBoxLayout()
        BtnLayout = QtGui.QHBoxLayout()
        self.dataDocked = QtGui.QWidget()

        self.FileNameRdOnlyBox()
        self.BrowseButton()
        self.GraphFittingOneButton()
        self.GraphFittingOneCheckBox()

        FileHLayout.addWidget(self.fileNameLabel)
        FileHLayout.addWidget(self.rdOnlyFileName)
        FileHLayout.addStretch(1)
        FileHLayout.addWidget(self.BrowseBtn)
        FileHLayout.addStretch(1)

        BtnLayout.addStretch(1)
        BtnLayout.addWidget(self.GraphFittingOneBtn)

        layout.addRow(FileHLayout)
        layout.addRow(self.graphCheckBx)
        layout.addRow(BtnLayout)
        self.dataDocked.setLayout(layout)
        self.dockDataGraphing.setWidget(self.dataDocked)

        # Adding the docked widget to the main window
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.dockDataGraphing)

    def restoreDockFittingOptionOne(self):
        """This funtion restores the Graphing Options Dock Widget for Fitting One, if it's closed"""
        if self.dockDataGraphing.isVisible() == False:
            self.dockFittingOptionOne()

    def GraphFittingOneCheckBox(self):
        """This function contains a group box with check boxes for fitting one"""
        self.graphCheckBx = QtGui.QGroupBox("Select graphs")

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

        self.checkBxAmplitude.stateChanged.connect(self.CheckGraphCheckBoxes)
        self.checkBxAmplitudeXWidth.stateChanged.connect(self.CheckGraphCheckBoxes)
        self.checkBxPeakWidth.stateChanged.connect(self.CheckGraphCheckBoxes)
        self.checkBxPeakPosition.stateChanged.connect(self.CheckGraphCheckBoxes)
        self.checkBxGraphAll.stateChanged.connect(self.CheckGraphCheckBoxes)

        self.graphCheckBx.setLayout(vbox)

    # ------------------------------------------------------------------------------------#
    def dockPlotRawData(self):
        """Function that creates the dockWidget, Graph Options for fitting one"""

        self.dockRawData = QtGui.QDockWidget("xPlotting Options", self)
        self.dockRawData.setFloating(False)
        self.dockRawData.setMaximumWidth(300)
        self.dockRawData.setAllowedAreas(QtCore.Qt.RightDockWidgetArea | QtCore.Qt.LeftDockWidgetArea)

        layout = QtGui.QFormLayout()
        FileHLayout = QtGui.QHBoxLayout()
        BtnLayout = QtGui.QHBoxLayout()
        self.dataDocked = QtGui.QWidget()

        self.FileNameRdOnlyBox()
        self.BrowseButton()
        self.GraphButton()
        self.RawDataPlotCheckBox()

        FileHLayout.addWidget(self.fileNameLabel)
        FileHLayout.addWidget(self.rdOnlyFileName)
        FileHLayout.addWidget(self.BrowseBtn)
        FileHLayout.addStretch(1)

        BtnLayout.addStretch(1)
        BtnLayout.addWidget(self.GraphBtn)

        layout.addRow(FileHLayout)
        layout.addRow(self.graphCheckBx)
        layout.addRow(BtnLayout)
        self.dataDocked.setLayout(layout)
        self.dockRawData.setWidget(self.dataDocked)

        # Adding the docked widget to the main window
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.dockRawData)

    def restoreDockPlotRawData(self):
        """This funtion restores the Graphing Options Dock Widget for Fitting One, if it's closed"""
        if self.dockRawData.isVisible() == False:
            self.dockFittingOptionOne()

    def RawDataPlotCheckBox(self):
        """This function contains a group box with check boxes"""
        self.graphCheckBx = QtGui.QGroupBox("Select graphs")

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

        self.checkBxAmplitude.stateChanged.connect(self.CheckGraphCheckBoxes)
        self.checkBxAmplitudeXWidth.stateChanged.connect(self.CheckGraphCheckBoxes)
        self.checkBxPeakWidth.stateChanged.connect(self.CheckGraphCheckBoxes)
        self.checkBxPeakPosition.stateChanged.connect(self.CheckGraphCheckBoxes)
        self.checkBxGraphAll.stateChanged.connect(self.CheckGraphCheckBoxes)

        self.graphCheckBx.setLayout(vbox)

    # ---------------------------------------------------------------------------------------------#
    def windowTabs(self):
        """This function creates the central widget QTabWidget and creates the Data tab"""
        self.tabWidget = QtGui.QTabWidget()
        self.tabBar = QtGui.QTabBar()

        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.closeTab)


    def closeTab(self, tabIndex):
        """This method closes the tab and closes the canvas. A garbage collector is used
        to collect the left memory.
        :param tabIndex: is the index of the tab
        """
        self.figArray[tabIndex].clear()
        self.figArray.pop(tabIndex)
        self.canvasArray[tabIndex].renderer.clear()
        del self.canvasArray[tabIndex].renderer
        self.canvasArray[tabIndex].mpl_disconnect(self.canvasArray[tabIndex].scroll_pick_id)
        self.canvasArray[tabIndex].mpl_disconnect(self.canvasArray[tabIndex].button_pick_id)
        self.canvasArray[tabIndex].close()
        self.canvasArray.pop(tabIndex)
        gc.collect()

        self.tabWidget.removeTab(tabIndex)

    # ------------------------------------------------------------------------------------#
    def FileNameRdOnlyBox(self):
        """This method contains a QLineEdit and label that display the selected file
            next to the browse button"""
        self.rdOnlyFileName = QtGui.QLineEdit()
        self.rdOnlyFileName.setReadOnly(True)
        self.rdOnlyFileName.setTextMargins(0, 0, 10, 0)
        self.rdOnlyFileName.setFixedWidth(125)

        self.fileNameLabel = QtGui.QLabel()
        self.fileNameLabel.setText("File Name:")

    # ------------------------------------------------------------------------------------#
    def GraphFittingOneButton(self):
        """Funtion that creates a graph button, connects to the GraphData() method"""
        self.GraphFittingOneBtn = QtGui.QPushButton('Graph', self)
        self.GraphFittingOneBtn.clicked.connect(self.GraphDataFittingOne)
        self.GraphFittingOneBtn.setStatusTip("Graphs the check graphs")

    def BrowseButton(self):
        """Funtion that creates a browse method, connects to the openFile() method"""
        # Button next to the FileNameRdOnly label and LineEdit
        self.BrowseBtn = QtGui.QPushButton('Browse', self)
        self.BrowseBtn.clicked.connect(self.openFile)
        self.BrowseBtn.setStatusTip("Browse and open an existing file")
    # ------------------------------------------------------------------------------------#

    def SetupComponents(self):
        """ Function to setup status bar and menu bar
        """
        self.myStatusBar = QtGui.QStatusBar()
        self.setStatusBar(self.myStatusBar)
        self.myStatusBar.showMessage('Ready', 30000)

        self.CreateActions()
        self.CreateMenus()
        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAction)
        self.graphMenu.addAction(self.graphRawData)
        self.graphMenu.addAction(self.graphingFittingOne)

        self.helpMenu.addSeparator()  
        self.helpMenu.addAction(self.aboutAction)

    def CreateActions(self):
        """Function that creates the actions used in the menu bar"""
        self.openAction = QtGui.QAction(QtGui.QIcon('openFolder.png'), '&Open',
                                        self, shortcut=QtGui.QKeySequence.Open,
                                        statusTip="Open an existing file",
                                        triggered=self.openFile)
        self.exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), 'E&xit',
                                        self, shortcut="Ctrl+Q",
                                        statusTip="Exit the Application",
                                        triggered=self.exitFile)
        self.graphingFittingOne= QtGui.QAction('Fitting One',
                                                   self, statusTip="Dock the graphing options",
                                                   triggered=self.restoreDockFittingOptionOne)
        self.graphRawData= QtGui.QAction('Raw Data',
                                            self, statusTip="Plots different graphs for the raw data")
        self.aboutAction = QtGui.QAction(QtGui.QIcon('about.png'), 'A&bout',
                                         self, shortcut="Ctrl+B", statusTip="Displays info about the graph program",
                                         triggered=self.aboutHelp)

    def CreateMenus(self):
        """This is where I initialize the menu bar and create the menus"""
        self.mainMenu = self.menuBar()
        self.fileMenu = self.mainMenu.addMenu("File")
        self.graphMenu = self.mainMenu.addMenu("Graph")
        self.helpMenu = self.mainMenu.addMenu("Help")
    # ---------------------------------------------------------------------------------------------#

    def openFile(self):
        """This method opens the file """
        openDlg = QtGui.QFileDialog()
        self.fileName = openDlg.getOpenFileName()

        self.rdOnlyFileName.setText(self.fileName)
        self.rdOnlyFileName.setStatusTip(self.fileName)

    def exitFile(self):
        response = self.msgApp("Exiting Form", "Would you like to exit the form")

        if response == "Y":
            self.close()
        else:
            pass

    def msgApp(self, title, msg):
        userInfo = QtGui.QMessageBox.question(self, title, msg, QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

        if userInfo == QtGui.QMessageBox.Yes:
            return "Y"
        if userInfo == QtGui.QMessageBox.No:
            return "N"

    def aboutHelp(self):
        QtGui.QMessageBox.about(self, "About Data Graphing",
                          "Open a file and select the graphs you want to graph, "
                          "then click to graph the graphs. If you close down the "
                          "graphing options you can click on the ")

    # -----------------------------------------------------------------------------------------#

    def CheckGraphCheckBoxes(self):
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
    # -----------------------------------------------------------------------------------------#
    def graphAmplitude(self):
        """This method graphs the Amplitude graph"""
        if self.fileName is not None:
            if os.path.isfile(self.fileName):
                mainGraph = QtGui.QWidget()

                dpi = 100
                fig = Figure((5.0, 4.0), dpi=dpi)
                canvas = FigureCanvas(fig)
                canvas.setParent(mainGraph)

                data = np.loadtxt(open(self.fileName))
                axes = fig.add_subplot(111)

                yy0 = data[:, 0]
                yy_err0 = data[:, 1]
                xx = [-7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 7, 6, 5, 4, 3, 2, 1, 0, -1, -2, -3, -4, -5, -6,
                      -7]
                axes.plot(xx, yy0)
                axes.errorbar(xx, yy0, yerr=yy_err0, fmt='o')
                axes.set_title('Amplitude')
                canvas.draw()

                tab = QtGui.QWidget()
                tab.setStatusTip("Amplitude graph")
                vbox = QtGui.QVBoxLayout()
                graphNavigationBar = NavigationToolbar(canvas, self)
                vbox.addWidget(graphNavigationBar)
                vbox.addWidget(canvas)
                tab.setLayout(vbox)

                self.tabWidget.addTab(tab, "Amplitude")

                self.canvasArray.append(canvas)
                self.figArray.append(fig)


    # -----------------------------------------------------------------------------------------#
    def graphPeakPosition(self):
        """This method graphs the Peak and position graph"""
        if self.fileName is not None:
            if os.path.isfile(self.fileName):
                mainGraph = QtGui.QWidget()

                dpi = 100
                fig = Figure((5.0, 4.0), dpi=dpi)
                canvas = FigureCanvas(fig)
                canvas.setParent(mainGraph)

                data = np.loadtxt(open(self.fileName))
                axes = fig.add_subplot(111)

                xx = [-7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 7, 6, 5, 4, 3, 2, 1, 0, -1, -2, -3, -4, -5, -6,
                      -7]
                yy1 = data[:, 2]
                yy_err1 = data[:, 3]
                axes.plot(xx, yy1)
                axes.errorbar(xx, yy1, yerr=yy_err1, fmt='o')
                axes.set_title('Peak Position')
                canvas.draw()

                tab = QtGui.QWidget()
                tab.setStatusTip("Peak position graph")

                vbox = QtGui.QVBoxLayout()
                graphNavigationBar = NavigationToolbar(canvas, self)
                vbox.addWidget(graphNavigationBar)
                vbox.addWidget(canvas)
                tab.setLayout(vbox)

                self.tabWidget.addTab(tab, "Peak Position")


                self.canvasArray.append(canvas)
                self.figArray.append(fig)

    # ----------------------------------------------------------------------------------------------------#
    def graphPeakWidth(self):
        """This method graphs the Peak width graph"""
        if self.fileName is not None:
            if os.path.isfile(self.fileName):
                mainGraph = QtGui.QWidget()

                dpi = 100
                fig = Figure((5.0, 4.0), dpi=dpi)
                canvas = FigureCanvas(fig)
                canvas.setParent(mainGraph)

                data = np.loadtxt(open(self.fileName))
                axes = fig.add_subplot(111)

                xx = [-7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 7, 6, 5, 4, 3, 2, 1, 0, -1, -2, -3, -4, -5, -6,
                      -7]
                yy2 = data[:, 4]
                yy_err2 = data[:, 5]
                axes.plot(xx, yy2)
                axes.errorbar(xx, yy2, yerr=yy_err2, fmt='o')
                axes.set_title('Peak Width')
                canvas.draw()

                tab = QtGui.QWidget()
                tab.setStatusTip("Peak width graph")
                vbox = QtGui.QVBoxLayout()
                graphNavigationBar = NavigationToolbar(canvas, self)
                vbox.addWidget(graphNavigationBar)
                vbox.addWidget(canvas)
                tab.setLayout(vbox)
                self.tabWidget.addTab(tab, "Peak Width")

                self.canvasArray.append(canvas)
                self.figArray.append(fig)

    # ----------------------------------------------------------------------------------------------------#
    def graphAmplitudeXWidth(self):
        """This method graphs the amplitude x width graph"""
        if self.fileName is not None:
            if os.path.isfile(self.fileName):
                mainGraph = QtGui.QWidget()

                dpi = 100
                fig = Figure((5.0, 4.0), dpi=dpi)
                canvas = FigureCanvas(fig)
                canvas.setParent(mainGraph)

                data = np.loadtxt(open(self.fileName))
                axes = fig.add_subplot(111)

                xx = [-7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 7, 6, 5, 4, 3, 2, 1, 0, -1, -2, -3, -4, -5, -6,
                      -7]
                yy2 = data[:, 4]
                yy0 = data[:, 0]
                yy3 = yy0 * yy2
                axes.plot(xx, yy3)
                axes.plot(xx, yy3, 'go')
                axes.set_title('Amplitude Times Width')
                canvas.draw()

                tab = QtGui.QWidget()
                tab.setStatusTip("Amplitude times width graph")
                vbox = QtGui.QVBoxLayout()
                graphNavigationBar = NavigationToolbar(canvas, self)
                vbox.addWidget(graphNavigationBar)
                vbox.addWidget(canvas)
                tab.setLayout(vbox)
                self.tabWidget.addTab(tab, "Amplitude Times Width")

                self.canvasArray.append(canvas)
                self.figArray.append(fig)

    # ------------------------------------------------------------------------------------------------------------#
    def graphAll(self):
        """Fuction graphs all the graphs. Makes sure the fileName is not empty
            and that the path leads to a file
        """
        if self.fileName is not None:
            if os.path.isfile(self.fileName):
                self.graphAmplitude()
                self.graphPeakPosition()
                self.graphPeakWidth()
                self.graphAmplitudeXWidth()

    # -----------------------------------------------------------------------------------------#
    def GraphDataFittingOne(self):
        """Function that graphs the information from the file and calls on the different method to graph
        depending on the check boxes the user has chosen. Checks for the fileName not to be empty and
        the path to lead to an actual file.
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
                    self.graphAmplitude()

                if self.checkBxPeakPosition.isChecked() and self.checkBxGraphAll.isChecked() == False:
                    self.graphPeakPosition()

                if self.checkBxPeakWidth.isChecked() and self.checkBxGraphAll.isChecked() == False:
                    self.graphPeakWidth()

                if self.checkBxAmplitudeXWidth.isChecked() and self.checkBxGraphAll.isChecked() == False:
                    self.graphAmplitudeXWidth()

                if self.checkBxGraphAll.isChecked():
                   self.graphAll()

        self.checkBxGraphAll.setCheckState(QtCore.Qt.Unchecked)
        self.checkBxAmplitude.setCheckState(QtCore.Qt.Unchecked)
        self.checkBxAmplitudeXWidth.setCheckState(QtCore.Qt.Unchecked)
        self.checkBxPeakPosition.setCheckState(QtCore.Qt.Unchecked)
        self.checkBxPeakWidth.setCheckState(QtCore.Qt.Unchecked)
    # ---------------------------------------------------------------------------------------------------#
    def  GraphRawData(self):
        self.PlotColorGraphRawData()

    def PlotColorGraphRawData(self):
        if self.fileName is not None:
            if os.path.isfile(self.fileName):
                mainGraph = QtGui.QWidget()

                dpi = 100
                fig = Figure((3.0, 3.0), dpi=dpi)
                canvas = FigureCanvas(fig)
                canvas.setParent(mainGraph)
                axes = fig.add_subplot(111)

                print(self.fileName)
                title0 = 'file:'
                # read file header
                inF = open(self.fileName, 'r')
                lines = inF.readlines()
                header = ''
                for (iL, line) in enumerate(lines):
                    if line.startswith('#'):
                        header = line
                inF.close()
                data = np.loadtxt(open(self.fileName))
                #    print data.shape, header
                words = header.split()
                ampl = ''
                if len(words) > 6:
                    ampl = words[6]
                # line1 = '[0] --> [-' +str(ampl) + '] --> [0] --> [+'+str(ampl) + '] --> [0]'
                line1 = '[-' + str(ampl) + '] --> [0] --> [+' + str(ampl) + '] --> [0] --> [-' + str(ampl) + '] '
                title0 = title0 + '\n' + header  # + '\t' + line1
                nRow = data.shape[0]  # Gets the number of rows
                nCol = data.shape[1]  # Gets the number of columns
                x = 0
                for f in range(nCol):
                    if (np.mean(data[:, f]) == 0):
                        pass
                    else:
                        x += 1
                nCol = x

                TT = np.zeros((nRow, nCol))
                for i in range(nCol):
                    TT[:, i] = data[:, i]

                tMax = np.max(TT)
                tMin = np.min(TT)

                z = np.linspace(tMin, tMax, endpoint=True)
                YY = range(nCol)
                XX = range(nRow)

                axes.contourf(YY, XX, TT, z)
                fig.colorbar(axes.contourf(YY, XX, TT, z))
                axes.set_title(title0)
                axes.set_xlabel('array_index (voltage:' + line1 + ')')
                axes.set_ylabel('spec_pnt: L')

                canvas.draw()

                tab = QtGui.QWidget()
                tab.setStatusTip("Raw Data")
                vbox = QtGui.QVBoxLayout()
                graphNavigationBar = NavigationToolbar(canvas, self)
                vbox.addWidget(graphNavigationBar)
                vbox.addWidget(canvas)
                tab.setLayout(vbox)
                self.tabWidget.addTab(tab, "Raw Data")

                self.canvasArray.append(canvas)
                self.figArray.append(fig)


def main():
    """Main method"""
    app = QtGui.QApplication(sys.argv)
    myMainWindow = MainWindow()
    myMainWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()