from Qt import QtCore, QtGui, QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui 
import maya.cmds as cmds
import sys

import LegoBrick

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class LegoDialog(QtWidgets.QDialog):

    dlg_instance = None
    
    @classmethod
    def show_dialog(cls):
        if not cls.dlg_instance:
            cls.dlg_instance = LegoDialog()
        
        if cls.dlg_instance.isHidden():
            cls.dlg_instance.show()
        else:
            cls.dlg_isntance.raise_()
            cls.dlg_instance.activateWindow()

    def __init__(self, parent=maya_main_window()):
        super(LegoDialog, self).__init__(parent)

        self.setWindowTitle("Lego Generator")
        self.setMinimumSize(500, 500)
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)

        self.current_bricks = None

        self.create_widgets()
        self.create_layouts()
        self.create_connections()
    
    def create_widgets(self):
        self.tower_rb = QtWidgets.QRadioButton("Tower")
        self.wall_rb = QtWidgets.QRadioButton("Wall")

        self.spin_box = QtWidgets.QSpinBox()
        self.spin_box.setFixedWidth(80)
        self.spin_box.setMinimum(0)
        self.spin_box.setMaximum(100)
        self.spin_box.setSingleStep(1)
        #self.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)

        self.add_brick_btn = QtWidgets.QPushButton("Add Brick(s)")

    def create_layouts(self):
        radio_btn_layout = QtWidgets.QHBoxLayout()
        radio_btn_layout.addWidget(self.tower_rb)
        radio_btn_layout.addWidget(self.wall_rb)

        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Number of Bricks:", self.spin_box)
        form_layout.addRow("", radio_btn_layout)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.add_brick_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(radio_btn_layout)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

    def create_connections(self):
        self.add_brick_btn.clicked.connect(self.add_bricks)

        self.spin_box.valueChanged.connect(self.build_tower)

    def add_bricks(self):
        if (self.tower_rb.toggled):
            self.build_tower(self.spin_box.value)
        else:
            self.build_wall(self.spin_box.value)

    def build_tower(self, height):
        if (self.current_bricks != None):
            cmds.select(self.current_bricks)
            cmds.delete()
            self.current_bricks = None
        
        for i in range(height):
            brick = LegoBrick(2, 2)
            brick.create_brick()
            brick.move_brick(0, 096 * i, 0)
            self.current_bricks.append(brick.get_brick())

    def build_wall(self, length):
        pass

if __name__ == "__main__":
    try: 
        lego_dialog.close()
        lego_dialog.deleteLater()
    except:
        pass

    lego_dialog = LegoDialog()
    lego_dialog.show()