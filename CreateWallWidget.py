from Qt import QtCore, QtGui, QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
import maya.cmds as cmds

import sys
import importlib
import random

sys.path.append("C:\\Users\\abiga\\OneDrive\\Documents\\maya\\2024\\plug-ins")
sys.path.append("C:\\Users\\dennin.a\\OneDrive - Northeastern University\\Documents\\maya\\2024\\plug-ins")

from maya_lego_plugin import LegoBrick
from maya_lego_plugin import LegoColors
from maya_lego_plugin import ColorPalette

importlib.reload(LegoBrick)
importlib.reload(LegoColors)
importlib.reload(ColorPalette)

class CreateWallWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(CreateWallWidget, self).__init__(parent)
    
        self.current_bricks = []
        self.old_height = 1
        self.old_width = 1
        self.height = 1
        self.width = 1
        self.brick_count = 1

        self.colors = LegoColors.LegoColors().get_colors()
        
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

        self.random_colors_rb = QtWidgets.QRadioButton("Random Colors")
        self.select_color_rb = QtWidgets.QRadioButton("Select Color")
        self.select_color_set_rb = QtWidgets.QRadioButton("Select Color Set")

        self.randomize_bricks_cb = QtWidgets.QCheckBox("Random Bricks")

        self.color_palette = ColorPalette.ColorPalette()

        self.add_wall_btn = QtWidgets.QPushButton("Add Wall")

    def create_layouts(self):
        width_layout = QtWidgets.QHBoxLayout()
        width_layout.addWidget(self.width_sb)
        width_layout.addWidget(self.width_slider)

        height_layout = QtWidgets.QHBoxLayout()
        height_layout.addWidget(self.height_sb)
        height_layout.addWidget(self.height_slider)

        create_wall_layout = QtWidgets.QFormLayout()
        create_wall_layout.addRow("", self.create_wall_btn)

        color_layout = QtWidgets.QHBoxLayout()
        color_layout.addWidget(self.random_colors_rb)
        color_layout.addWidget(self.select_color_rb)
        color_layout.addWidget(self.select_color_set_rb)

        self.color_palette.set_visible(False)

        add_wall_layout = QtWidgets.QFormLayout()
        add_wall_layout.addRow("Height: ", height_layout)
        add_wall_layout.addRow("Width: ", width_layout)
        add_wall_layout.addRow("Colors: ", color_layout)
        add_wall_layout.addRow("", self.color_palette)
        add_wall_layout.addRow("", self.randomize_bricks_cb)
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
        self.create_wall_btn.clicked.connect(self.create_wall)

        self.height_sb.valueChanged.connect(self.height_slider.setValue)
        self.height_slider.valueChanged.connect(self.height_sb.setValue)

        self.width_sb.valueChanged.connect(self.width_slider.setValue)
        self.width_slider.valueChanged.connect(self.width_sb.setValue)

        self.height_sb.valueChanged.connect(self.set_height)
        self.width_sb.valueChanged.connect(self.set_width)

        self.random_colors_rb.toggled.connect(self.color_btn_handler)
        self.select_color_rb.toggled.connect(self.color_btn_handler)

        self.add_wall_btn.clicked.connect(self.add_wall)
        
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

    def color_btn_handler(self):
        if self.random_colors_rb.isChecked():
            self.color_palette.set_visible(False)
        elif self.select_color_rb.isChecked():
            self.color_palette.set_visible(True)

    def create_random_wall(self): 
        wall = [[' '] * (self.width * 2) for _ in range(self.height)]  # Initialize wall with empty spaces

        def can_place_brick_of_length(i, j, length):
            # Check if the brick of 'length' can be placed starting from position (i, j)
            if j + length <= (self.width * 2):
                for x in range(length):
                    if wall[i][j + x] != ' ':
                        return False
                return True
            return False

        def place_brick_of_length(i, j, length):
            # Place the brick of 'length' starting from position (i, j)
            for x in range(length):
                if x == 0: 
                    wall[i][j + x] = length
                else:
                    wall[i][j + x] = '/'
                
                
        def find_next_position():
            # Find the next empty position in the wall
            positions = [(i, j) for i in range(self.height) for j in range(self.width * 2)]
            random.shuffle(positions)
            for i, j in positions:
                if wall[i][j] == ' ':
                    return i, j
            return None, None

        while True:
            # Find the next empty position in the wall
            i, j = find_next_position()
            if i is None:
                break

            # Randomly choose between small and regular bricks
            brick_length = random.choice([1, 2, 3, 4])

            # Check if the chosen brick can be placed
            if can_place_brick_of_length(i, j, brick_length):
                place_brick_of_length(i, j, brick_length)

        col = 0
        for row in wall:

            distance = 0

            for x in row:
                if x != '/':
                    brick = LegoBrick.LegoBrick(x, 2, rand_color=True)
                    brick.create_brick("brick_{0}x2_".format(x))
                    
                    bounding_box = cmds.xform(brick.get_brick(), q=1, bb=1, ws=1)
                    x_min, y_min, z_min, x_max, y_max, z_max = bounding_box
                    cmds.move(x_min, [brick.get_brick() + '.scalePivot', brick.get_brick() + '.rotatePivot'], x = 1, absolute = 1)
                    cmds.move(y_min, [brick.get_brick() + '.scalePivot', brick.get_brick() + '.rotatePivot'], y=1, )
                    
                    brick.move_brick(x_min * -1, 0, 0)
                    brick.move_brick((distance + (x_min * -1)), .96 * col, 0)
                    cmds.xform(brick.get_brick(), cp = 1)

                    distance = x_max + distance + (x_min * -1)

            col = col + 1

        return wall

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
                    selected = self.current_bricks[row][col - 1]
                    
                    cmds.select(selected)
                    self.brick_count = self.brick_count - len(selected)
                    cmds.delete()
                    self.current_bricks[row] = self.current_bricks[row][0:col - 1]

        self.old_height = self.height
        self.old_width = self.width

    def add_wall(self):
        if self.randomize_bricks_cb.isChecked():
            selected = []
            
            for row in range(0, self.height):
                selected = self.current_bricks[row]
                cmds.select(selected)
                cmds.delete()

            self.current_bricks = []
            self.create_random_wall()

        self.wall_reset()

    def wall_reset(self):
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