#!/usr/bin/env python

"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.
"""

# --------------------------------------------------------------------------------------#
from __future__ import unicode_literals
import sys
import numpy as np
from pylab import *
from matplotlib.backends import qt_compat
use_pyside = qt_compat.QT_API == qt_compat.QT_API_PYSIDE
if use_pyside:
    from PySide import QtGui, QtCore
else:
    from PyQt4 import QtGui, QtCore
from scipy.optimize import curve_fit
from scipy import exp
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar

class GaussianFitting:

    def __init__ (self, parent=None):
        self.TwoPkFitData = [0][0]
        self.dockedOpt = parent
        self.myMainWindow = self.dockedOpt.myMainWindow

    # --------------------------------------------------------------------------------------#
    def TwoPeakFitting(self, filename):
        """Gaussian Fitting for Two Peaks [Updated April 4, 2017]"""
        data = np.loadtxt(open(filename))
        nRow = data.shape[0]  # Number of rows
        nCol = data.shape[1]  # Number of columns
        x = 0
        for f in range(nCol):
            if (np.mean(data[:, f]) == 0):
                pass
            else:
                x += 1
        nCol = x  # Gets the number of columns with data in them

        TT = np.zeros((nRow, nCol))
        for i in range(nCol):
            TT[:, i] = data[:, i]

        self.PkFitData = zeros((nCol, 12))  # Creats the empty 2D List

        for j in range(nCol):
            col_data = data[:, j]
            xx = arange(0, len(col_data))
            param = self.twoPkFitting(xx, col_data)
            fit_result = param[0]
            fit_error = param[1]

            self.PkFitData[j, :] = (fit_result[0], fit_error[0], fit_result[1], fit_error[1], fit_result[2],
                                     fit_error[2], fit_result[3], fit_error[3], fit_result[4], fit_error[4],
                                     fit_result[5], fit_error[5])
        print(self.PkFitData)


    def twoPkFitting(self, xx, yy):
        mean = sum(xx * yy) / sum(yy)
        sigma = np.sqrt(sum(yy * (xx - mean) ** 2)) / sqrt(sum(yy))
        bg0 = min(yy)  # min value of yy
        popt, pcov = curve_fit(self.gaus2, xx, yy, p0=[self.peak1Amp, self.peak2Amp, self.peak1Pos, self.peak2Pos,
                                                       self.peak1Wid, self.peak2Wid, bg0])
        perr = np.sqrt(np.diag(pcov))
        return popt, perr


    def gaus2(self, x, a1, a2, x01, x02, sigma1, sigma2, background):
        return a1 * exp(-(x - x01) ** 2 / (2 * sigma1 ** 2))\
               + a2 *exp(-(x - x02) ** 2 / (2 * sigma2 ** 2)) + background

    # -----------------------------------------------------------------------------------------------------------#
    def OnePeakFitting(self, filename):
        """Gaussian Fit for one Peak [Updated April 11, 2017]"""
        data = np.loadtxt(open(filename))
        nRow = data.shape[0]  # num of points, 76
        nCol = data.shape[1]  # size of array from epics, 100
        x = 0
        for f in range(nCol):
            if (np.mean(data[:, f]) == 0):
                pass
            else:
                x += 1
        nCol = x  # Gets the number of columns

        TT = np.zeros((nRow, nCol))
        for i in range(nCol):
            TT[:, i] = data[:, i]

        self.PkFitData = zeros((nCol, 6))  # Creates the empty 2D List
        for j in range(nCol):
            col_data = data[:, j]
            xx = arange(0, len(col_data))
            param = self.OnePkFitting(xx, col_data)
            fit_result = param[0]
            fit_error = param[1]
            self.PkFitData[j, :] =(fit_result[0], fit_error[0], fit_result[1], fit_error[1], fit_result[2],
                                             fit_error[2])
            print(self.PkFitData)


    def OnePkFitting(self, xx, yy):
        n = len(xx)  # the number of data
        mean = sum(xx * yy) / sum(yy)  # note this correction
        #    #sigma = sum(y*(x-mean)**2)/n        #note this correction
        sigma = np.sqrt(sum(yy * (xx - mean) ** 2)) / sqrt(sum(yy))
        popt, pcov = curve_fit(self.gaus1, xx, yy, p0=[1000, mean, sigma, 1, 100])
        perr = np.sqrt(np.diag(pcov))
        return popt, perr


    def gaus1(self, x, a, x0, sigma, a0, b):
        return a * exp(-(x - x0) ** 2 / (2 * sigma ** 2)) + a0 * x + b

    # -----------------------------------------------------------------------------------------------------------#
    def graphAmplitude(self):
        """This method graphs the Amplitude graph"""

        mainGraph = QtGui.QWidget()

        dpi = 100
        fig = Figure((5.0, 4.0), dpi=dpi)
        canvas = FigureCanvas(fig)
        canvas.setParent(mainGraph)

        axes = fig.add_subplot(111)

        yy0 = self.PkFitData[:, 0]
        yy_err0 = self.PkFitData[:, 1]
        xx = [-7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4,5,6,7,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7]

        axes.plot(xx, yy0)
        axes.errorbar(xx, yy0, yerr=yy_err0, fmt='o')
        axes.set_title('Amplitude')
        canvas.draw()

        tab = QtGui.QWidget()
        tab.setStatusTip("Amplitude graph")
        vbox = QtGui.QVBoxLayout()
        graphNavigationBar = NavigationToolbar(canvas, mainGraph)
        vbox.addWidget(graphNavigationBar)
        vbox.addWidget(canvas)
        tab.setLayout(vbox)

        self.myMainWindow.tabWidget.addTab(tab, "Amplitude")
        self.myMainWindow.tabWidget.setCurrentWidget(tab)

        self.myMainWindow.canvasArray.append(canvas)
        self.myMainWindow.figArray.append(fig)
    # -----------------------------------------------------------------------------------------#

    def graphPeakPosition(self):
        """This method graphs the Peak and position graph"""

        mainGraph = QtGui.QWidget()

        dpi = 100
        fig = Figure((5.0, 4.0), dpi=dpi)
        canvas = FigureCanvas(fig)
        canvas.setParent(mainGraph)

        axes = fig.add_subplot(111)

        xx = [-7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 7, 6, 5, 4, 3, 2, 1, 0, -1, -2, -3, -4, -5, -6,
              -7]
        yy1 = self.PkFitData[:, 2]
        yy_err1 = self.PkFitData[:, 3]
        axes.plot(xx, yy1)
        axes.errorbar(xx, yy1, yerr=yy_err1, fmt='o')
        axes.set_title('Peak Position')
        canvas.draw()

        tab = QtGui.QWidget()
        tab.setStatusTip("Peak position graph")

        vbox = QtGui.QVBoxLayout()
        graphNavigationBar = NavigationToolbar(canvas, mainGraph)
        vbox.addWidget(graphNavigationBar)
        vbox.addWidget(canvas)
        tab.setLayout(vbox)

        self.myMainWindow.tabWidget.addTab(tab, "Peak Position")
        self.myMainWindow.tabWidget.setCurrentWidget(tab)

        self.myMainWindow.canvasArray.append(canvas)
        self.myMainWindow.figArray.append(fig)

    # ----------------------------------------------------------------------------------------------------#

    def graphPeakWidth(self):
        """This method graphs the Peak width graph"""

        mainGraph = QtGui.QWidget()

        dpi = 100
        fig = Figure((5.0, 4.0), dpi=dpi)
        canvas = FigureCanvas(fig)
        canvas.setParent(mainGraph)

        axes = fig.add_subplot(111)

        xx = [-7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 7, 6, 5, 4, 3, 2, 1, 0, -1, -2, -3, -4, -5, -6,
              -7]
        yy2 = self.PkFitData[:, 4]
        yy_err2 = self.PkFitData[:, 5]
        axes.plot(xx, yy2)
        axes.errorbar(xx, yy2, yerr=yy_err2, fmt='o')
        axes.set_title('Peak Width')
        canvas.draw()

        tab = QtGui.QWidget()
        tab.setStatusTip("Peak width graph")
        vbox = QtGui.QVBoxLayout()
        graphNavigationBar = NavigationToolbar(canvas, mainGraph)
        vbox.addWidget(graphNavigationBar)
        vbox.addWidget(canvas)
        tab.setLayout(vbox)
        self.dockedOpt.myMainWindow.tabWidget.addTab(tab, "Peak Width")
        self.dockedOpt.myMainWindow.tabWidget.setCurrentWidget(tab)

        self.dockedOpt.myMainWindow.canvasArray.append(canvas)
        self.dockedOpt.myMainWindow.figArray.append(fig)

    # ----------------------------------------------------------------------------------------------------#
    def graphAmplitudeXWidth(self):
        """This method graphs the amplitude x width graph"""

        mainGraph = QtGui.QWidget()

        dpi = 100
        fig = Figure((5.0, 4.0), dpi=dpi)
        canvas = FigureCanvas(fig)
        canvas.setParent(mainGraph)
        axes = fig.add_subplot(111)

        xx = [-7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 7, 6, 5, 4, 3, 2, 1, 0, -1, -2, -3, -4, -5, -6,
              -7]
        yy2 = self.PkFitData[:, 4]
        yy0 = self.PkFitData[:, 0]
        yy3 = yy0 * yy2
        axes.plot(xx, yy3)
        axes.plot(xx, yy3, 'go')
        axes.set_title('Amplitude Times Width')
        canvas.draw()

        tab = QtGui.QWidget()
        tab.setStatusTip("Amplitude times width graph")
        vbox = QtGui.QVBoxLayout()
        graphNavigationBar = NavigationToolbar(canvas, mainGraph)
        vbox.addWidget(graphNavigationBar)
        vbox.addWidget(canvas)
        tab.setLayout(vbox)
        self.dockedOpt.myMainWindow.tabWidget.addTab(tab, "Amplitude Times Width")
        self.dockedOpt.myMainWindow.tabWidget.setCurrentWidget(tab)

        self.dockedOpt.myMainWindow.canvasArray.append(canvas)
        self.dockedOpt.myMainWindow.figArray.append(fig)

    # ------------------------------------------------------------------------------------------------------------#
    def graphAll(self):
        """Fuction graphs all the graphs. Makes sure the fileName is not empty
            and that the path leads to a file
        """

        self.graphAmplitude()
        self.graphPeakPosition()
        self.graphPeakWidth()
        self.graphAmplitudeXWidth()
    # ------------------------------------------------------------------------------___#
    def gausInputDialog(self):
        """Dialog where the user import """
        self.dialogGausFit = QtGui.QDialog()
        inputForm = QtGui.QFormLayout()
        buttonLayout = QtGui.QHBoxLayout()
        spaceLayout = QtGui.QVBoxLayout()

        spaceLayout.addStretch(1)

        self.peak1AmpSpin = QtGui.QSpinBox()
        self.peak1AmpSpin.setMaximum(100000)
        self.peak1PosSpin = QtGui.QSpinBox()
        self.peak1WidthSpin = QtGui.QSpinBox()

        self.peak2AmpSpin = QtGui.QSpinBox()
        self.peak2AmpSpin.setMaximum(100000)
        self.peak2PosSpin = QtGui.QSpinBox()
        self.peak2WidthSpin = QtGui.QSpinBox()

        ok = QtGui.QPushButton("Ok")
        cancel = QtGui.QPushButton("Cancel")

        cancel.clicked.connect(self.dialogGausFit.close)
        ok.clicked.connect(self.returnGausUserInput)
        buttonLayout.addWidget(cancel)
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(ok)

        inputForm.addRow("Peak#1 Amplitude: ", self.peak1AmpSpin)
        inputForm.addRow("Peak#1 Position: ", self.peak1PosSpin)
        inputForm.addRow("Peak#1 Width: ", self.peak1WidthSpin)
        inputForm.addRow("Peak#2 Amplitude: ", self.peak2AmpSpin)
        inputForm.addRow("Peak#2 Position: ", self.peak2PosSpin)
        inputForm.addRow("Peak#2 Width: ", self.peak2WidthSpin)
        inputForm.addRow(spaceLayout)
        inputForm.addRow(buttonLayout)

        self.dialogGausFit.setWindowTitle("Input Guess Data for Fit")
        self.dialogGausFit.setLayout(inputForm)
        self.dialogGausFit.setGeometry(300,200, 250, 200)
        self.dialogGausFit.exec_()

    def returnGausUserInput(self):
        """Sets the values of the variables in the method twoPkFitting, that are used as parameters.
        It also sets the Gaussian fit options available"""
        self.peak1Amp = float(self.peak1AmpSpin.value())
        self.peak1Pos = float(self.peak1PosSpin.value())
        self.peak1Wid = float(self.peak1WidthSpin.value())

        self.peak2Amp = float(self.peak2AmpSpin.value())
        self.peak2Pos = float(self.peak2PosSpin.value())
        self.peak2Wid = float(self.peak2WidthSpin.value())

        self.dialogGausFit.close()
        self.TwoPeakFitting(self.dockedOpt.fileName)
        self.dockedOpt.dockGaussianFitOptions()
        self.dockedOpt.rdOnlyFileNameG.setText(self.dockedOpt.fileName)
        self.dockedOpt.rdOnlyFileNameG.setStatusTip(self.dockedOpt.fileName)



