#!/usr/bin/env python

"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.

#C In some methods LFit or L refer to the Lattice Constant not RLU
"""
# ---------------------------------------------------------------------------------------------------------------------#
from __future__ import unicode_literals
import sys
import os
import numpy as np
from pylab import *

from matplotlib.backends import qt_compat
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
import gc


from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from DockedOptions import DockedOption
# ---------------------------------------------------------------------------------------------------------------------#

class MainWindow (QMainWindow):
    """Initializes the main window with the central tab widget. It also has the graphing methods for the raw data and
    creating a report.
    """

    def __init__ (self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setGeometry(50, 50, 1000, 800)
        self.setMinimumSize(800, 700)
        self.setWindowTitle("xPlot Util")
        self.setWindowIcon(QIcon('Icons/Graph.png'))
        self.dockedOpt = DockedOption(parent=self)
        self.gausFit = self.dockedOpt.gausFit
        self.readSpec = self.dockedOpt.readSpec
        self.algebraExp = self.gausFit.algebraExp
        self.canvasArray = []
        self.figArray = []

        self.SetupComponents()
        self.windowTabs()
        self.dockedOpt.DockMainOptions()
        self.setCentralWidget(self.tabWidget)
        self.setTabPosition(Qt.RightDockWidgetArea | Qt.LeftDockWidgetArea, QTabWidget.North)

    # -----------------------------Central Tab Widget------------------------------------------------------------------#
    def windowTabs(self):
        """This function creates the central widget QTabWidget.
        """
        self.tabWidget = QTabWidget()

        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.closeTab)


    def closeTab(self, tabIndex):
        """This method closes the tab and closes the canvas. A garbage collector is used
        to collect the left memory.
        :param tabIndex: index of the tab
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

    def savingCanvasTabs(self,tab, name, canvas, fig):
        """This method adds the tab widget to the tab widget, and it adds the canvas and fig to arrays.
        :param tab: QWidget
        :param name: name of tab
        :param canvas: graph canvas
        :param fig: graph figure
        """
        self.tabWidget.addTab(tab, name)
        self.tabWidget.setCurrentWidget(tab)

        self.canvasArray.append(canvas)
        self.figArray.append(fig)

    # --------------------------------------Menu Bar and Such----------------------------------------------------------#
    def SetupComponents(self):
        """ Function to setups status bar and menu bar
        """
        self.myStatusBar = QStatusBar()
        self.setStatusBar(self.myStatusBar)
        self.myStatusBar.showMessage('Ready', 3000)

        self.CreateActions()
        self.CreateMenus()
        self.fileMenu.addAction(self.openAction)
        self.exportMenu = self.fileMenu.addMenu("Export")
        self.exportMenu.addAction(self.reportAction)
        self.exportMenu.addAction(self.binGausFitReportAction)
        self.fileMenu.addAction(self.resetAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAction)
        self.graphMenu.addAction(self.mainOptionsAction)
        self.graphMenu.addAction(self.normalizeAction)
        self.graphMenu.addAction(self.algebraicExpAction)
        self.graphMenu.addAction(self.GaussianFitAction)
        self.graphMenu.addAction(self.LatticeFitAction)
        self.graphMenu.addSeparator()
        self.helpMenu.addSeparator()  
        self.helpMenu.addAction(self.aboutAction)

        self.LatticeFitAction.setEnabled(False)

    def CreateActions(self):
        """Function that creates the actions used in the menu bar
        """
        self.openAction = QAction(QIcon('openFolder.png'), '&Open',
                                        self, shortcut=QKeySequence.Open,
                                        statusTip="Open an existing file",
                                        triggered=self.readSpec.openSpecFile)
        self.exitAction = QAction(QIcon('exit.png'), 'E&xit',
                                        self, shortcut="Ctrl+Q",
                                        statusTip="Exit the Application",
                                        triggered=self.exitFile)
        self.resetAction = QAction('Reset', self, statusTip="Resets xPlot Util",
                                  triggered=self.dockedOpt.resetxPlot)
        self.reportAction = QAction('Report', self, statusTip="Create a report of the data",
                                         triggered=self.ReportDialog)
        self.binGausFitReportAction = QAction('Bin Gaussian Fit', self, statusTip="Create a report from bin fitted data",
                                              triggered=self.gausFit.EachFitDataReport)
        self.mainOptionsAction = QAction('Main Options', self, statusTip="Main options for xPlot Util",
                                             triggered=self.dockedOpt.restoreMainOptions)
        self.GaussianFitAction= QAction('Gaussian Fit',self, statusTip="Dock the graphing options" ,
                                        triggered=self.dockedOpt.WhichPeakGaussianFit)
        self.LatticeFitAction = QAction('Lattice Fit', self, statusTip="Fits the data to the L fit",
                                  triggered =self.dockedOpt.GraphingLatticeOptionsTree)
        self.normalizeAction = QAction('Normalize', self, statusTip ='Normalizes the data',
                                       triggered=self.readSpec.NormalizerDialog)
        self.algebraicExpAction = QAction('Algebraic Expressions', self, statusTip='Algebraic expressions.',
                                       triggered=self.dockedOpt.DataGraphingAlgebraicExpOptionsTree)
        self.aboutAction = QAction(QIcon('about.png'), 'A&bout',
                                         self, shortcut="Ctrl+B", statusTip="Displays info about the graph program",
                                         triggered=self.aboutHelp)

    def CreateMenus(self):
        """This is where I initialize the menu bar and create the menus
        """
        self.mainMenu = self.menuBar()
        self.fileMenu = self.mainMenu.addMenu("File")
        self.graphMenu = self.mainMenu.addMenu("xPlot")
        self.helpMenu = self.mainMenu.addMenu("Help")

    def exitFile(self):
        """Exit method that closes the program.
        """
        response = self.dockedOpt.msgApp("Exiting Form", "Would you like to exit the form")

        if response == "Y":
            self.close()
        else:
            pass

    def aboutHelp(self):
        """Talks briefly about the program.
        """
        """This needs further development. In it's infancy level. """
        QMessageBox.about(self, "About xPlot Util",
                          "Click on the browse button to select and open a spec file.\n"
                          "Choose a PVValue and under xPlot in the menu bar you can click\n on the fits. "
                          "Once you've clicked on the fit, checkboxes will apear that\n will enable you "
                          "to graph")

    # ----------------------------------------Raw Data Graphs----------------------------------------------------------#
    def PlotColorGraphRawData(self):
        """This function uses the raw data to plot a color graph of the data.
        """
        # Reads file header for voltage
        inF = open(self.dockedOpt.fileName, 'r')
        lines = inF.readlines()
        header = ''
        for (iL, line) in enumerate(lines):
            if line.startswith('#'):
                header = line
        inF.close()
        words = header.split()
        ampl = ''
        if len(words) > 6:
            ampl = words[6]
        line1 = '[-' + str(ampl) + '] --> [0] --> [+' + str(ampl) + '] --> [0] --> [-' + str(ampl) + '] '

        if self.readSpec.lMax - self.readSpec.lMin == 0:
            xx = range(len(self.readSpec.L))
            yLabel = 'Points'
        else:
            xx = self.readSpec.L
            yLabel = "RLU (Reciprocal Lattice Unit)"

        gTitle = 'Raw Data Color Graph (Scan#: ' + self.readSpec.scan + ')'
        statTip = "Raw Data Color Graph"
        xLabel = 'Bins (voltage:' + line1 + ')'
        tabName = 'Raw Data Color Graph'
        whichG = 'C'

        self.GraphUtilRawDataLineGraphs(gTitle, xLabel, yLabel, statTip, tabName, xx, whichG)

    def ColorGraphContrastDialog(self):
        """This method creates a dialog with dynamically created radio buttons from the spec file, which allow the
        user to pick which chamber was used to normalize.
        """
        if self.dockedOpt.normalizingStat == False and self.dockedOpt.FileError() == False :
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

            self.normalizeDialog.setWindowTitle("Normalize raw data")
            self.normalizeDialog.setLayout(dialogBox)
            self.normalizeDialog.resize(250, 250)
            self.normalizeDialog.exec_()

    def GraphUtilRawDataLineGraphs(self, gTitle, xLabel, yLabel, statTip, tabName, xx, whichG):
        """Generic graph method that helps graph the raw data.
        :param gTitle: Title of the graph
        :param xLabel: x-axis label
        :param yLabel: y-axis label
        :param statTip: status tip
        :param tabName: tab name
        :param xx: x-axis values
        :param whichG: char to know which graph to plot
        """
        mainGraph = QWidget()
        fig = Figure((3.0, 3.0), dpi=100)
        canvas = FigureCanvas(fig)

        canvas.setParent(mainGraph)
        axes = fig.add_subplot(111)

        nRow = self.dockedOpt.TT.shape[0]  # Gets the number of rows
        nCol = self.dockedOpt.TT.shape[1]

        if whichG == 'L':
            for j in range(nCol):
                yy = self.dockedOpt.TT[:, j]
                axes.plot(xx, yy)
        elif whichG == 'C':
            tMax = np.max(self.dockedOpt.TT)
            tMin = np.min(self.dockedOpt.TT)
            z = np.linspace(tMin, tMax)
            yy = range(nCol)
            """data = np.loadtxt("text")
            nRow = data.shape[0]  # Gets the number of rows
            nCol = data.shape[1]  # Gets the number of columns
            x = 0
            for f in range(nCol):
                if (np.mean(data[:, f]) == 0):
                    break
                else:
                    x += 1
            nCol = x
            txt = np.zeros((nRow, nCol))
            for i in range(nCol):
                txt[:, i] = data[:, i]
            print len(txt[1, :])
            xx = 1.982, 1.984, 1.986, 1.988, 1.99, 1.992, 1.994, 1.996, 1.998, 2, 2.002, 2.004,\
                 2.006, 2.008, 2.01, 2.012, 2.014, 2.016, 2.018, 2.02, 2.022, 2.024, 2.026, 2.028
            yy = range(20)
            tMax = np.max(txt)
            tMin = np.min(txt)
            z = np.linspace(tMin, tMax)"""
            axes.contourf(yy, xx, self.dockedOpt.TT, z)
            fig.colorbar(axes.contourf(yy, xx, self.dockedOpt.TT, z))

            contrastBtn = QPushButton("Contrast")
            contrastBtn.clicked.connect(self.normalizeDialog.close)


        axes.set_title(gTitle)
        axes.set_xlabel(xLabel)
        axes.set_ylabel(yLabel)
        canvas.draw()

        tab = QWidget()
        tab.setStatusTip(statTip)
        vbox = QVBoxLayout()
        graphNavigationBar = NavigationToolbar(canvas, self)
        vbox.addWidget(graphNavigationBar)
        vbox.addWidget(canvas)
        tab.setLayout(vbox)

        self.savingCanvasTabs(tab, tabName, canvas, fig)

    def PlotLineGraphRawData(self):
        """This method graphs the raw data into a line graph with the x-axis the user picks.
        """
        xx, gTitle, xLabel, statTip, tabName = self.readSpec.getRawDataLinePlotElements()
        if gTitle != 0:
             self.GraphUtilRawDataLineGraphs(gTitle, xLabel, 'Intensity', statTip, tabName, xx, 'L')

    # -----------------------------------Creating Report---------------------------------------------------------------#
    def ReportButton(self):
        """This button creates a report.
        """
        self.reportBtn = QPushButton('Report', self)
        self.reportBtn.setStatusTip("Creates a report of the chosen data.")
        self.reportBtn.clicked.connect(self.CreateReport)

    def CancelReportButton(self):
        """This button cancels the creation of a report.
        """
        self.cancelReportBtn = QPushButton('Cancel', self)
        self.cancelReportBtn.setStatusTip("Cancels the creation of the report.")
        self.cancelReportBtn.clicked.connect(self.reportDialog.close)

    def CreateReport(self):
        """This method calls on the save file dialog and once the file has been selected it writes out the report.
        """
        if self.reportCbGausFit.isChecked() or self.reportCbLFit.isChecked():
            self.reportDialog.close()
            selectedFilters = ".txt"
            self.reportFile, self.reportFileFilter = QFileDialog.getSaveFileName(self, "Save Report", "",
                                                                                 selectedFilters)
            if self.reportFile != "":
                self.reportFile += self.reportFileFilter
                self.WritingReport()

    def ReportDialog(self):
        """Dialog that allows the user to select the data it wants on the report.
        """
        self.reportDialog = QDialog(self)
        vBox = QVBoxLayout()
        buttonLayout = QHBoxLayout()

        self.ReportCheckBox()
        self.CancelReportButton()
        self.ReportButton()

        buttonLayout.addWidget(self.cancelReportBtn)
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(self.reportBtn)

        vBox.addWidget(self.reportGroupBx)
        vBox.addLayout(buttonLayout)

        self.reportDialog.setWindowTitle("Create Final Report")
        self.reportDialog.setLayout(vBox)
        self.reportDialog.exec_()

    def ReportCheckBox(self):
        """This method creates the check boxes used in the report dialog.
        """
        self.reportGroupBx = QGroupBox("Select the data")

        self.reportCbGausFit = QCheckBox("Gaussian Fit")
        self.reportCbLFit = QCheckBox("Lattice Fit")
        self.reportCbGausFit.setEnabled(False)
        self.reportCbLFit.setEnabled(False)

        if self.dockedOpt.gausFitStat == True:
            self.reportCbGausFit.setEnabled(True)
        if self.dockedOpt.LFitStat == True:
            self.reportCbLFit.setEnabled(True)

        vbox = QVBoxLayout()
        vbox.addWidget(self.reportCbGausFit)
        vbox.addWidget(self.reportCbLFit)

        self.reportGroupBx.setLayout(vbox)

    def WritingReport(self):
        """This method writes the data to the report file, calling on the appropriate methods. It's important to
        note that the report can only contain data from the gaussian fit and the lattice fit.
        """
        _, nCol = self.dockedOpt.fileInfo()
        reportData = np.zeros((nCol, 0))
        header = "#H "
        scanNum = self.readSpec.scan
        comment = "#C PVvalue #" + scanNum + "\n"

        if self.reportCbGausFit.isChecked():
            if self.dockedOpt.onePeakStat == True:
                header += "Amp Err Position Err Width Err "
                reportData = np.concatenate((reportData, self.gausFit.OnePkFitData), axis=1)
            if self.dockedOpt.twoPeakStat == True:
                header += "Amp Err Amp Err Pos Err Pos Err Wid Err Wid Err "
                reportData = np.concatenate((reportData, self.gausFit.TwoPkGausFitData), axis=1)

        if self.reportCbLFit.isChecked():
            if self.dockedOpt.onePeakStat == True:
                header += "Lattice Lattice% "
                # Reshapes the array so that it can be append
                L = np.reshape(self.gausFit.LPosData, (len(self.gausFit.LPosData), 1))  # Enables array to be appended
                LPrc = np.reshape(self.gausFit.LPosPrcChangeData, (len(self.gausFit.LPosPrcChangeData), 1))
                reportData = np.concatenate((reportData, L, LPrc), axis=1)
            if self.dockedOpt.twoPeakStat == True:
                header += "Lattice1 Lattice2 Lattice1% Lattice2% "
                L1 = np.reshape(self.gausFit.LPos1Data, (len(self.gausFit.LPos1Data), 1))  # Reshapes to append
                L2 = np.reshape(self.gausFit.LPos2Data, (len(self.gausFit.LPos2Data), 1))  # Reshapes to append
                L1Prc = np.reshape(self.gausFit.LPos1PrcChangeData, (len(self.gausFit.LPos1PrcChangeData), 1))
                L2Prc = np.reshape(self.gausFit.LPos2PrcChangeData, (len(self.gausFit.LPos2PrcChangeData), 1))

                reportData = np.concatenate((reportData, L1, L2, L1Prc, L2Prc), axis=1)

        # Writes to sheet
        np.savetxt(self.reportFile, reportData, fmt=str('%f'), header=header, comments=comment)

def main():
    """Main method.
    """
    app = QApplication(sys.argv)
    myMainWindow = MainWindow()
    myMainWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()