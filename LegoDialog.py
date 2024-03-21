from Qt import QtCore, QtGui, QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui 
import maya.cmds as cmds
import sys
import importlib

sys.path.append("C:\\Users\\abiga\\OneDrive\\Documents\\maya\\2024\\plug-ins")

from maya_lego_plugin import LegoBrick

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
        self.brick_count = 1

        self.create_widgets()
        self.create_layouts()
        self.create_connections()
    
    def create_widgets(self):
        self.create_wall_btn = QtWidgets.QPushButton("Create Wall")
        
        self.width_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.width_sb = QtWidgets.QSpinBox()
        self.width_sb.setMinimum(1)
        self.width_sb.setMaximum(100)

        self.height_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.height_sb = QtWidgets.QSpinBox()
        self.height_sb.setMinimum(1)
        self.height_sb.setMaximum(100)

        self.interlocking_cb = QtWidgets.QCheckBox()

        self.add_wall_btn = QtWidgets.QPushButton("Add Wall")

    def create_layouts(self):
        width_layout = QtWidgets.QHBoxLayout()
        width_layout.addWidget(self.width_sb)
        width_layout.addWidget(self.width_slider)

        height_layout = QtWidgets.QHBoxLayout()
        height_layout.addWidget(self.height_sb)
        height_layout.addWidget(self.height_slider)

        create_wall_layout = QtWidgets.QFormLayout()
        create_wall_layout.addRow("Interlocking: ", self.interlocking_cb)
        create_wall_layout.addRow("", self.create_wall_btn)

        add_wall_layout = QtWidgets.QFormLayout()
        add_wall_layout.addRow("Height: ", height_layout)
        add_wall_layout.addRow("Width: ", width_layout)
        add_wall_layout.addRow("", self.add_wall_btn)

        self.create_wall_frame = QtWidgets.QFrame()
        self.create_wall_frame.setLayout(create_wall_layout)

        self.add_wall_frame = QtWidgets.QFrame()
        self.add_wall_frame.setLayout(add_wall_layout)
        self.add_wall_frame.hide()
    
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.create_wall_frame)
        main_layout.addWidget(self.add_wall_frame)

    def create_connections(self):
        self.create_wall_btn.clicked.connect(self.set_wall_type)
        self.add_wall_btn.clicked.connect(self.add_wall)
        
        self.height_sb.valueChanged.connect(self.height_slider.setValue)
        self.height_slider.valueChanged.connect(self.height_sb.setValue)

        self.width_sb.valueChanged.connect(self.width_slider.setValue)
        self.width_slider.valueChanged.connect(self.width_sb.setValue)

        self.height_sb.valueChanged.connect(self.set_height)
        self.width_sb.valueChanged.connect(self.set_width)
    
    def set_height(self):
        self.height = self.height_sb.value()
        
        if self.interlocking_cb.isChecked():
            self.create_interlocking_wall()
        else:
            self.create_wall()
    
    def set_width(self):
        self.width = self.width_sb.value()

        if self.interlocking_cb.isChecked():
            self.create_interlocking_wall()
        else:
            self.create_wall()

    def set_wall_type(self):
        if self.interlocking_cb.isChecked():
            self.create_interlocking_wall()
        else: 
            self.create_wall()

    def create_interlocking_wall(self):
        self.create_wall_frame.hide()
        self.add_wall_frame.show()

        if len(self.current_bricks) == 0:
            brick = LegoBrick.LegoBrick(2, 2)
            brick.create_brick("brick_2x2_")
            self.current_bricks.append(brick.get_brick())
        
        width_increased = self.width > self.old_width
        height_increased = self.height > self.old_height

        old_width_even = self.old_width % 2 == 0
        old_height_even = self.old_height % 2 == 0

        width_even = self.width % 2 == 0
        height_even = self.height % 2 == 0
        

        ######################################################
        if width_increased: 
            if width_even:
                if old_width_even:
                    #if not height_even:
                    # OLD WIDTH: EVEN -> NEW WIDTH: EVEN, HEIGHT: ODD
                    # Add 2 x 4s to fill in until it is at new width
                    for col in range(self.old_width, self.width, 2):
                        brick = LegoBrick.LegoBrick(4, 2)
                        brick.create_brick("brick_2x4_")
                        brick.move_brick(.16 * 10 * col, 0, 0)
                        self.current_bricks.append(brick.get_brick())

                    # else:
                    #     # OLD WIDTH: EVEN -> NEW WIDTH: EVEN, HEIGHT: EVEN
                    #     # Add 2x4s to fill it in?
                    #     pass
                            
                else:
                    if not height_even:
                    # OLD WIDTH: ODD -> NEW WIDTH: EVEN, HEIGHT: ODD
                    # Delete the 2x2 at the end, replace with 2x4 (and fill in necessary 2x4s)
                        cmds.select(self.current_bricks[-1])
                        self.current_bricks = self.current_bricks[0:len(self.current_bricks) - 1]
                        cmds.delete()
                        
                        for col in range(self.old_width, self.width, 2):
                            brick = LegoBrick.LegoBrick(4, 2)
                            brick.create_brick("brick_2x4_")
                            brick.move_brick(.16 * 10 * col, 0, 0)
                            self.current_bricks.append(brick.get_brick())

                    # OLD WIDTH: ODD -> NEW WIDTH: EVEN, HEIGHT: EVEN
                    # Shift everything over 1 unit, replace first brick with 4x2?
                    else:
                        for col in range(1, self.width):
                            tmp_brick = self.current_bricks[col]
                            cmds.move_brick(.16 * 10 * col, 0, 0)


            elif not width_even:
                if old_width_even:
                    # if the old width was even and new width is odd, add 2x2
                    for col in range(self.old_width, self.width, 2):
                        brick = LegoBrick.LegoBrick(2, 2)
                        brick.create_brick("brick_2x2_")
           
                        brick.move_brick(.16 * 10 * (col + 0.5), 0, 0)
                        self.current_bricks.append(brick.get_brick())
                elif self.width > 2:
                    # if the old width was odd and the new width is odd, remove 2x2, add 2x4, add 2x2
                    cmds.select(self.current_bricks[-1])
                    self.current_bricks = self.current_bricks[0:len(self.current_bricks) - 1]
                    cmds.delete()
                    
                    for col in range(self.old_width, self.width - 1):
                        brick = LegoBrick.LegoBrick(4, 2)
                        brick.create_brick("brick_2x4_")
           
                        brick.move_brick(.16 * 10 * col, 0, 0)
                        self.current_bricks.append(brick.get_brick())
                    
                    brick = LegoBrick.LegoBrick(2, 2)
                    brick.create_brick("brick_2x2_")
           
                    brick.move_brick(.16 * 10 * (col + 0.5), 0, 0)
                    self.current_bricks.append(brick.get_brick())




        # # FOR ODD LAYER HEIGHT
        # elif self.height % 2 != 0:
        #     # for now assuming one layer
            

        # # FOR EVEN LAYER HEIGHT            
        # else:
        #     pass




        self.old_width = self.width
        self.old_height = self.height

    def create_wall(self):
        self.create_wall_frame.hide()
        self.add_wall_frame.show()
        
        if len(self.current_bricks) == 0: 
            brick = LegoBrick.LegoBrick(2, 2)
            brick.create_brick("brick_2x2_{0}".format(self.brick_count))
            self.current_group = cmds.group(brick.get_brick(), name="wall")
            self.current_bricks.append([brick.get_brick()])

        if self.height > self.old_height:
            for row in range(self.old_height, self.height):
                curr_row = []
                for col in range(0, self.width):
                    brick = LegoBrick.LegoBrick(2, 2)
                    self.brick_count = self.brick_count + 1
                    brick.create_brick("brick_2x2_{0}".format(self.brick_count))
                    brick.move_brick(.16 * 10 * col, .96 * row, 0)
                    curr_row.append(brick.get_brick())
                    cmds.parent(brick.get_brick(), self.current_group)

                self.current_bricks.append(curr_row)

        elif self.width > self.old_width:
            for row in range(self.height):
                for col in range(self.old_width, self.width):
                    brick = LegoBrick.LegoBrick(2, 2)
                    self.brick_count = self.brick_count + 1
                    brick.create_brick("brick_2x2_{0}".format(self.brick_count))
                    brick.move_brick(.16 * 10 * col, .96 * row, 0)
                    self.current_bricks[row].append(brick.get_brick())
                    cmds.parent(brick.get_brick(), self.current_group)

        elif self.height < self.old_height:
            for row in range(self.height, self.old_height):
                selected = self.current_bricks[row]
                cmds.select(selected)
                self.brick_count = self.brick_count - len(selected)
                cmds.delete()
            
            self.current_bricks = self.current_bricks[0:self.height]

        elif self.width < self.old_width:
            selected = []
            for row in range(self.height):
                for col in range(self.old_width, self.width, -1):
                    print(row)
                    print(col)
                    print(self.current_bricks[row])
                    selected = self.current_bricks[row][col - 1]
                    
                    cmds.select(selected)
                    self.brick_count = self.brick_count - len(selected)
                    cmds.delete()
                    self.current_bricks[row] = self.current_bricks[row][0:col - 1]

        self.old_height = self.height
        self.old_width = self.width

    def add_wall(self):
        self.old_width = 1
        self.old_height = 1
        self.height = 1
        self.width = 1
        self.height_sb.setValue(1)
        self.width_sb.setValue(1)
        self.brick_count = 1
        self.current_bricks = []
        self.current_group = None
        self.create_wall_frame.show()
        self.add_wall_frame.hide()

if __name__ == "__main__":
    try: 
        lego_dialog.close()
        lego_dialog.deleteLater()
    except:
        pass

    lego_dialog = LegoDialog()
    lego_dialog.show()