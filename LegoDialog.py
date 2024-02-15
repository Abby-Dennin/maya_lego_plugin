from Qt import QtCore, QtGui, QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui 
import maya.cmds as cmds
import sys

sys.path.append("C:\\Users\\abiga\\OneDrive\\Documents\\maya\\2024\\plug-ins\\maya_lego_plugin")

from maya_lego_plugin import LegoBrick
import importlib
importlib.reload(LegoBrick)

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

        self.current_bricks = []
        self.old_height = 1
        self.old_width = 1
        
        self.height = 1
        self.width = 1

        self.create_widgets()
        self.create_layouts()
        self.create_connections()
    
    def create_widgets(self):
        self.create_wall_btn = QtWidgets.QPushButton("Create Wall")
        
        self.height_sb = QtWidgets.QSpinBox()
        self.height_sb.setFixedWidth(80)
        self.height_sb.setMinimum(1)
        self.height_sb.setMaximum(100)
        
        self.width_sb = QtWidgets.QSpinBox()
        self.width_sb.setFixedWidth(80)
        self.width_sb.setMinimum(1)
        self.width_sb.setMaximum(100)

        #self.height_sb.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)

        self.add_wall_btn = QtWidgets.QPushButton("Add Wall")

    def create_layouts(self):
       

        create_wall_layout = QtWidgets.QFormLayout()
        create_wall_layout.addRow("Height: ", self.height_sb)
        create_wall_layout.addRow("Width: ", self.width_sb)
        create_wall_layout.addRow("", self.add_wall_btn)

        self.create_wall_frame = QtWidgets.QFrame()
        self.create_wall_frame.setLayout(create_wall_layout)
        self.create_wall_frame.hide()
    
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.create_wall_btn)
        main_layout.addWidget(self.create_wall_frame)

    def create_connections(self):
        self.create_wall_btn.clicked.connect(self.create_wall)
        self.add_wall_btn.clicked.connect(self.add_wall)
        
        self.height_sb.valueChanged.connect(self.set_height)
        self.width_sb.valueChanged.connect(self.set_width)
    
    def set_height(self):
        self.height = self.height_sb.value()
        self.create_wall()
    
    def set_width(self):
        self.width = self.width_sb.value()
        self.create_wall()
        
    def create_wall(self):
        self.create_wall_btn.hide()
        self.create_wall_frame.show()
        
        if len(self.current_bricks) == 0: 
            brick = LegoBrick.LegoBrick(2, 2)
            brick.create_brick()

            self.current_bricks.append([brick.get_brick()])

        if self.height > self.old_height:
            for row in range(self.old_height, self.height):
                curr_row = []
                for col in range(0, self.width):
                    brick = LegoBrick.LegoBrick(2, 2)
                    brick.create_brick()
                    brick.move_brick(.16 * 10 * col, .96 * row, 0)
                    curr_row.append(brick.get_brick())

                self.current_bricks.append(curr_row)

        elif self.width > self.old_width:
            for row in range(self.height):
                for col in range(self.old_width, self.width):
                    brick = LegoBrick.LegoBrick(2, 2)
                    brick.create_brick()
                    brick.move_brick(.16 * 10 * col, .96 * row, 0)
                    self.current_bricks[row].append(brick.get_brick())
            
        elif self.height < self.old_height:
            selected = cmds.select(self.current_bricks[self.height:self.old_height][0])
            cmds.delete()

            self.current_bricks = self.current_bricks[0:self.height]

        elif self.width < self.old_width:
            selected = []
            for row in range(self.height):
                for col in range(self.width, self.old_width):
                    selected.append(self.current_bricks[row][col])
                    self.current_bricks[row] = self.current_bricks[row][0:col]

            cmds.select(selected)
            cmds.delete()

        self.old_height = self.height
        self.old_width = self.width

    def add_wall(self):
        self.create_wall_frame.hide()
        self.current_bricks = []
        self.old_width = 1
        self.old_height = 1
        self.height = 1
        self.width = 1
        self.create_wall_btn.show()

if __name__ == "__main__":
    try: 
        lego_dialog.close()
        lego_dialog.deleteLater()
    except:
        pass

    lego_dialog = LegoDialog()
    lego_dialog.show()