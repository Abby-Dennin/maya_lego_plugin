from Qt import QtCore, QtGui, QtWidgets
from shiboken2 import wrapInstance

from maya import cmds 
import sys
import importlib

sys.path.append("C:\\Users\\abiga\\OneDrive\\Documents\\maya\\2024\\plug-ins")

from maya_lego_plugin import LegoColors

importlib.reload(LegoColors)

class ColorPalette(QtWidgets.QWidget):
    
    def __init__(self, parent=None):
        super(ColorPalette, self).__init__(parent)

        lego_colors = LegoColors.LegoColors()

        self.colors = lego_colors.get_colors()
        self.color_btns = []


        self.create_widgets()
        self.create_layouts()

    def create_widgets(self):
        for color in self.colors:
            base_color_hex = color['hex']
            base_color_rgb = tuple(int(base_color_hex[i:i+2], 16) for i in (0, 2, 4))

            buttonStyle = "QPushButton{background-color: rgb(%s, %s, %s" % (base_color_rgb[0], base_color_rgb[1], base_color_rgb[2]) + "); }" 

            color_btn = QtWidgets.QPushButton()
            color_btn.setToolTip(color['name'])
            color_btn.setStyleSheet(buttonStyle)
            
            self.color_btns.append(color_btn)
    
    def create_layouts(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        color_layout = QtWidgets.QGridLayout()
  
        for i in range(0, 10):
            for j in range(0, 10):
                if ( i > 8 and j > 7):
                    pass
                else:
                    color_layout.addWidget(self.color_btns[j + (i * 10)], i, j)

        main_layout.addLayout(color_layout)
 

    


                
    

            
           