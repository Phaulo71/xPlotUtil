from mpl_toolkits.mplot3d import Axes3D, axes3d
import numpy as np
import matplotlib.pyplot as plt
from spec2nexus.spec import SpecDataFile
from PyQt5.QtWidgets import *
import pylab as plab
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Loading the data.
data = np.loadtxt("C:\\Users\\escal\\Downloads\\PVvalue.259")


# Loading Spec information for scan#: 259
# ========================================
specFile = SpecDataFile("C:\\Users\\escal\\Downloads\\pmnpt_1.spec")
l = specFile.scans["259"].data["L"]

########################################################################################################################
# Plotting the data in 3D


########################################################################################################################
fig1 = plt.figure()
ax = Axes3D(fig1)
ax.set_ylabel("Data")
ax.set_xlabel("Points")
ax.set_zlabel("L")
x = range(0, 64)  # This will have to be replaced by voltage
for i in range(0, 3721):
    z = np.full(64, l[i])
    y = data[i]
    ax.plot(x, y, zs=z)

fig1.show()


fig2 = plt.figure()
ax2 = Axes3D(fig2)
ax2.set_ylabel("Points")
ax2.set_xlabel("Data")
ax2.set_zlabel("L")
x = range(0, 64)  # This will have to be replaced by voltage
print(len(l))
print(len(data))
for i in range(0, 3721):
    z = np.full(64, l[i])
    y = data[i]
    ax2.plot(y, x, zs=z)

fig2.show()
########################################################################################################################

p,q,r = axes3d.get_test_data(0.05)
print(p)
print("q")

# WIREFRAME PLOT
########################################################################################################################
print("1")
window = QWidget()
print("2")
fig3 = plt.figure()
canvas = FigureCanvas(fig3)
#canvas.setParent(window)
navigationBar = NavigationToolbar(canvas, parent=window)
ax3 = Axes3D(fig3)
ax3.set_ylabel("L")
ax3.set_xlabel("Voltage")
ax3.set_zlabel("Data")

#  Getting arrays ready
print("Hello")
L = np.asarray(l)
y3 = np.array([L, ]*64).transpose()
x3 = np.array([np.asarray(range(0, 64)), ]*3721)
data = data
z3 = data
ax3.plot_wireframe(x3, y3, z3, rstride=50, cstride=15)
canvas.draw()

window.show()
########################################################################################################################