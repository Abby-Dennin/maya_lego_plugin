from Qt import QtCore, QtGui, QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui 
import maya.cmds as cmds
import sys

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

    def __init__(self, parent=maya_main_window):
        super(LegoDialog, self).__init__(parent)

        self.setWindowTitle("Lego Generator")
        self.setMinimumSize(500, 500)
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()
    
    def create_widgets(self):
        pass

    def create_layouts(self):
        pass

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