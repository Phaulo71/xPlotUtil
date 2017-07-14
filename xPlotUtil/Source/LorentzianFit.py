#!/usr/bin/env python

"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.

#C In some methods LFit or L refer to the Lattice Constant not RLU

"""
# ---------------------------------------------------------------------------------------------------------------------#
from __future__ import unicode_literals

from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import FormatStrFormatter
from peakutils import peak
from lmfit.models import LorentzianModel, GaussianModel, LinearModel, VoigtModel
from pylab import *
from scipy import exp
from scipy.optimize import curve_fit
# ---------------------------------------------------------------------------------------------------------------------#


class LorentzianFitting:
    """Contains Lorentzian and Voigt fit.
    """

    def __init__ (self, parent=None):
        self.algebraExp = parent
        self.gausFit = self.algebraExp.gausFit
        self.dockedOpt = self.algebraExp.dockedOpt
        self.readSpec = self.algebraExp.readSpec
        self.myMainWindow = self.algebraExp.myMainWindow

    def WhichPeakLorentzianFit(self):

        if self.dockedOpt.FileError() == False and self.dockedOpt.gausFitStat == False:
            chosePeak = self.dockedOpt.PeakDialog()
            if (chosePeak == 'One'):
                self.OnePeakLorentzianFit()
            elif (chosePeak == 'Two'):
                self.TwoPeakLorentzianFit()

    def OnePeakLorentzianFit(self):
        error = self.onePeakLorentzianFit()

        if error == False:
            self.dockedOpt.onePeakStat = True
            self.dockedOpt.gausFitStat = True
            self.dockedOpt.GraphingFitOptionsTree("L")

    def onePeakLorentzianFit(self):
        nRow, nCol = self.dockedOpt.fileInfo()

        self.gausFit.binFitData = zeros((nRow, 0))
        self.gausFit.OnePkFitData = zeros((nCol, 6))  # Creates the empty 2D List
        for j in range(nCol):
            yy = self.dockedOpt.TT[:, j]
            xx = arange(0, len(yy))

            x1 = xx[0]
            x2 = xx[-1]
            y1 = yy[0]
            y2 = yy[-1]
            m = (y2 - y1) / (x2 - x1)
            b = y2 - m * x2

            mod = GaussianModel()
            # print mod.param_names
            pars = mod.guess(yy, x=xx)
            mod = mod + LinearModel()
            pars.add('intercept', value=b, vary=True)
            pars.add('slope', value=m, vary=True)
            out = mod.fit(yy, pars, x=xx, slope=m)
            print pars
            # print out.best_values
            # print out.fit_report()
            # print out.eval()
            self.gausFit.OnePkFitData[j, :] = (out.best_values['amplitude'], 0, out.best_values['center'], 0,
                                               out.best_values['sigma'], 0)

            # Saves fitted data of each fit
            fitData = out.best_fit
            binFit = np.reshape(fitData, (len(fitData), 1))
            self.gausFit.binFitData = np.concatenate((self.gausFit.binFitData, binFit), axis=1)

            if self.gausFit.continueGraphingEachFit == True:
                self.gausFit.graphEachFitRawData(xx, yy, out.best_fit, 'L', 1)

        return False

    def index_of(arrval, value):
        "return index of array *at or below* value "
        if value < min(arrval):  return 0
        return max(np.where(arrval <= value)[0])

    def TwoPeakLorentzianFit(self):
        error = self.twoPeakLorentzianFit()

        if error == False:
            self.dockedOpt.twoPeakStat = True
            self.dockedOpt.fitStat = True
            self.dockedOpt.GraphingFitOptionsTree("L")

    def twoPeakLorentzianFit(self):
        nRow, nCol = self.dockedOpt.fileInfo()

        self.binFitData = zeros((nRow, 0))
        self.TwoPkGausFitData = zeros((nCol, 12))  # Creates the empty 2D List

        for j in range(nCol):
            yy = self.dockedOpt.TT[:, j]
            xx = arange(0, len(yy))

            x1 = xx[0]
            x2 = xx[-1]
            y1 = yy[0]
            y2 = yy[-1]
            m = (y2 - y1) / (x2 - x1)
            b = y2 - m * x2

            mod1 = VoigtModel(prefix='p1_')
            mod2 = VoigtModel(prefix='p2_')
            mod = mod1

            pars = mod.guess(yy, x=xx)
            pars2 = mod2.guess(yy, x=xx)
            mod = mod + mod2 + LinearModel()
            print pars1
            print pars2

            pars.add('intercept', value=b, vary=True)
            pars.add('slope', value=m, vary=True)
            out = mod.fit(yy, pars, x=xx, slope=m)
            print out
            # print mod.eval
        """ 
         #!/usr/bin/env python
            #<examples/doc_nistgauss2.py>
            import numpy as np
            from lmfit.models import GaussianModel, ExponentialModel
            
            import matplotlib.pyplot as plt
            
            dat = np.loadtxt('NIST_Gauss2.dat')
            x = dat[:, 1]
            y = dat[:, 0]
            
            exp_mod = ExponentialModel(prefix='exp_')
            gauss1  = GaussianModel(prefix='g1_')
            gauss2  = GaussianModel(prefix='g2_')
            
            def index_of(arrval, value):
                "return index of array *at or below* value "
                if value < min(arrval):  return 0
                return max(np.where(arrval<=value)[0])
            
            ix1 = index_of(x,  75)
            ix2 = index_of(x, 135)
            ix3 = index_of(x, 175)
            
            pars1 = exp_mod.guess(y[:ix1], x=x[:ix1])
            pars2 = gauss1.guess(y[ix1:ix2], x=x[ix1:ix2])
            pars3 = gauss2.guess(y[ix2:ix3], x=x[ix2:ix3])
            
            pars = pars1 + pars2 + pars3
            mod = gauss1 + gauss2 + exp_mod
            
            out = mod.fit(y, pars, x=x)
            
            print(out.fit_report(min_correl=0.5))
            
            plt.plot(x, y)
            plt.plot(x, out.init_fit, 'k--')
            plt.plot(x, out.best_fit, 'r-')
            plt.show()
            #<end examples/doc_nistgauss2.py>
        """


    def WhichPeakVoigtFit(self):

        if self.dockedOpt.FileError() == False and self.dockedOpt.gausFitStat == False:
            chosePeak = self.dockedOpt.PeakDialog()
            if (chosePeak == 'One'):
                self.OnePeakVoigtFit()
            elif (chosePeak == 'Two'):
                self.twoPeakVoigtFit()

    def OnePeakVoigtFit(self):
        error = self.onePeakVoigtFit()

        if error == False:
            self.dockedOpt.onePeakStat = True
            self.dockedOpt.gausFitStat = True
            self.dockedOpt.GraphingFitOptionsTree("V")

    def onePeakVoigtFit(self):
        nRow, nCol = self.dockedOpt.fileInfo()

        self.gausFit.binFitData = zeros((nRow, 0))
        self.gausFit.OnePkFitData = zeros((nCol, 6))  # Creates the empty 2D List
        for j in range(nCol):
            yy = self.dockedOpt.TT[:, j]
            xx = arange(0, len(yy))

            x1 = xx[0]
            x2 = xx[-1]
            y1 = yy[0]
            y2 = yy[-1]
            m = (y2 - y1) / (x2 - x1)
            b = y2 - m * x2

            mod = VoigtModel()
            # print mod.param_names
            pars = mod.guess(yy, x=xx)
            mod = mod + LinearModel()
            pars.add('intercept', value=b, vary=True)
            pars.add('slope', value=m, vary=True)
            out = mod.fit(yy, pars, x=xx, slope=m)
            print pars
            # print out.best_values
            # print out.fit_report()
            # print out.eval()
            self.gausFit.OnePkFitData[j, :] = (out.best_values['amplitude'], 0, out.best_values['center'], 0,
                                       out.best_values['sigma'], 0)

            # Saves fitted data of each fit
            fitData = out.best_fit
            binFit = np.reshape(fitData, (len(fitData), 1))
            self.gausFit.binFitData = np.concatenate((self.gausFit.binFitData, binFit), axis=1)

            if self.gausFit.continueGraphingEachFit == True:
                self.gausFit.graphEachFitRawData(xx, yy, out.best_fit, 'V', 1)

        return False

    def TwoPeakVoigtFit(self):
        error = self.twoPeakVoigtFit()

        if error == False:
            self.dockedOpt.twoPeakStat = True
            self.dockedOpt.fitStat = True
            self.dockedOpt.GraphingFitOptionsTree("V")

    def twoPeakVoigtFit(self):
        pass


