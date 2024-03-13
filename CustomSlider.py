from Qt import QtCore, QtGui, QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui 
import maya.cmds as cmds

class CustomSlider(QtWidgets.QWidget):
    def __init__(self):
        super(CustomSlider, self).__init__()
        
        self.create_widgets()
        self.create_layout()
        self.create_connections()
        
    def create_widgets(self):
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.numbox = QtWidgets.QSpinBox()

    def create_layout(self):
        layout = QtWidgets.QHBoxLayout(self)
 
        layout.addWidget(self.numbox)
        layout.addWidget(self.slider)
    
    def create_connections(self):
        self.slider.valueChanged.connect(self.numbox.setValue)
        self.slider.rangeChanged.connect(self.numbox.setRange)
        self.numbox.valueChanged.connect(self.slider.setValue)

    def setMinimum(self, min):
        self.slider.setMinimum(min)

    def setMaximum(self, max):
        self.slider.setMaximum(max)

    def setRange(self, min, max):
        self.slider.setRange(min, max)
    
    def setValue(self, value):
        self.slider.setValue(value)