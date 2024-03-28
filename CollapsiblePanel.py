from functools import partial
from Qt import QtCore, QtGui, QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
import maya.cmds as cmds

class PanelHeader(QtWidgets.QWidget):
    
    COLLAPSED_PIXMAP = QtGui.QPixmap(":teRightArrow.png")
    EXPANDED_PIXMAP = QtGui.QPixmap(":teDownArrow.png")

    clicked = QtCore.Signal()

    def __init__(self, text, parent=None):
        super(PanelHeader, self).__init__(parent)

        self.icon_label = QtWidgets.QLabel()
        self.icon_label.setFixedWidth(self.COLLAPSED_PIXMAP.width())
        
        self.text_label = QtWidgets.QLabel()

        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setContentsMargins(4, 4, 4, 4)
        self.main_layout.addWidget(self.icon_label)
        self.main_layout.addWidget(self.text_label)

        self.set_text(text)
        self.set_expanded(False)

    def set_text(self, text):
        self.text_label.setText("&nbsp;&nbsp;&nbsp;&nbsp;<b>{0}</b>".format(text))

    def is_expanded(self):
        return self._expanded
    
    def set_expanded(self, expanded):
        self._expanded = expanded

        if self._expanded:
            self.icon_label.setPixmap(self.EXPANDED_PIXMAP)
        else:
            self.icon_label.setPixmap(self.COLLAPSED_PIXMAP)

    def mouseReleaseEvent(self, event):
        self.clicked.emit()

class CollapsiblePanel(QtWidgets.QWidget):

    def __init__(self, text, parent=None):
        super(CollapsiblePanel, self).__init__(parent)

        self.header_wdg = PanelHeader(text)
        self.header_wdg.clicked.connect(self.on_header_clicked)
        self.body_wdg = QtWidgets.QWidget()

        self.body_layout = QtWidgets.QVBoxLayout(self.body_wdg)
        self.body_layout.setContentsMargins(4, 2, 4, 2)
        self.body_layout.setSpacing(3)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.header_wdg)
        self.main_layout.addWidget(self.body_wdg)

        self.set_expanded(False)
    
    def add_widget(self, widget): 
        self.body_layout.addWidget(widget)
    
    def add_layout(self, layout):
        self.body_layout.addLayout(layout)

    def set_expanded(self, expanded):
        self.header_wdg.set_expanded(expanded)
        self.body_wdg.setVisible(expanded)

    def on_header_clicked(self):
        self.set_expanded(not self.header_wdg.is_expanded())
