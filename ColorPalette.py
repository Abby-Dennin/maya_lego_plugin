from Qt import QtCore, QtGui, QtWidgets
from shiboken2 import wrapInstance

from maya import cmds 
import sys
import importlib

sys.path.append("C:\\Users\\abiga\\OneDrive\\Documents\\maya\\2024\\plug-ins")
sys.path.append("C:\\Users\\dennin.a\\OneDrive - Northeastern University\\Documents\\maya\\2024\\plug-ins")

from maya_lego_plugin import LegoColors

importlib.reload(LegoColors)

class ColorPalette(QtWidgets.QWidget):
    
    def __init__(self, parent=None):
        super(ColorPalette, self).__init__(parent)

        lego_colors = LegoColors.LegoColors()

        self.colors = lego_colors.get_colors()
        self.color_btns = []

        self.color_list = []

        self.curr_color = None

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):

        self.color_dlg = QtWidgets.QColorDialog()
        self.color_dlg.setOption(QtWidgets.QColorDialog.NoButtons, True)
        self.color_dlg.setOption(QtWidgets.QColorDialog.DontUseNativeDialog, True)

        index = 0
        for color in self.colors:
            base_color_hex = color['hex']
            base_color_rgb = tuple(int(base_color_hex[i:i+2], 16) for i in (0, 2, 4))

            self.color_dlg.setStandardColor(index, QtGui.QColor.fromRgb(base_color_rgb[0], base_color_rgb[1], base_color_rgb[2]))
            index = index + 1

            self.color_list.append({
                "name": color['name'],
                "hex": color['hex'],
                "qcolor": QtGui.QColor.fromRgb(base_color_rgb[0], base_color_rgb[1], base_color_rgb[2])
            })

    def create_layouts(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.color_dlg)
    
    def create_connections(self):
        self.color_dlg.currentColorChanged.connect(self.set_current_color)

    def set_visible(self, visible):
        self.color_dlg.setVisible(visible)

    def get_color(self):
        return self.color_dlg.getColor()
    
    def get_color_list(self):
        return self.color_list
    
    def set_current_color(self, color):
        for color_dict in self.color_list:
            if color_dict['qcolor'] == color:
                print(color_dict['name'])
                self.curr_color = color_dict
                return color_dict

    def get_curr_color(self):
        return self.curr_color
        



    


                
    

            
           