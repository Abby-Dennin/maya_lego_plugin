from Qt import QtCore, QtGui, QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui 
import maya.cmds as cmds
import sys
import importlib

sys.path.append("C:\\Users\\abiga\\OneDrive\\Documents\\maya\\2024\\plug-ins")

from maya_lego_plugin import LegoBrick
from maya_lego_plugin import CreateWallWidget
from maya_lego_plugin import CollapsiblePanel
from maya_lego_plugin import ColorPalette

importlib.reload(LegoBrick)
importlib.reload(CreateWallWidget)
importlib.reload(CollapsiblePanel)
importlib.reload(ColorPalette)

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

        self.create_widgets()
        self.create_layouts()
        self.create_connections()
    
    def create_widgets(self):
        self.body_wdg = QtWidgets.QWidget()
        self.create_wall_wdg = CreateWallWidget.CreateWallWidget()
        self.color_palette_wdg = ColorPalette.ColorPalette()

        self.create_wall_panel = CollapsiblePanel.CollapsiblePanel("Create Wall")
        self.create_wall_panel.add_widget(self.create_wall_wdg)

        self.color_palette_panel = CollapsiblePanel.CollapsiblePanel("Color Palette Test")
        self.color_palette_panel.add_widget(self.color_palette_wdg)

    def create_layouts(self):
        self.body_layout = QtWidgets.QVBoxLayout(self.body_wdg)
        self.body_layout.setContentsMargins(4, 2, 4, 2)
        self.body_layout.setSpacing(3)
        self.body_layout.setAlignment(QtCore.Qt.AlignTop)

        self.body_layout.addWidget(self.create_wall_panel)
        self.body_layout.addWidget(self.color_palette_panel)

        self.body_scroll_area = QtWidgets.QScrollArea()
        self.body_scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.body_scroll_area.setWidgetResizable(True)
        self.body_scroll_area.setWidget(self.body_wdg)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.body_scroll_area)

    def create_connections(self):
        pass

if __name__ == "__main__":
    try: 
        lego_dialog.close()
        lego_dialog.deleteLater()
    except:
        pass

    lego_dialog = LegoDialog()
    lego_dialog.show()