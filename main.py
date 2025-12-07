import sys
import os
from PyQt5.QtWidgets import  QApplication
from PyQt5.QtCore import Qt
from qfluentwidgets import Theme, setTheme
from qfluentwidgets import *
from src.ui.Window import Window
from qframelesswindow.utils import getSystemAccentColor

os.environ["QT_ENABLE_HIGHDPI_SCALING"]   = "1"
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
os.environ["QT_SCALE_FACTOR"]             = "0.75"
QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)


if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    app.setStyle('Windows')
    
    # Set default font size larger
    font = app.font('Segoe UI Variable')
    font.setPointSize(font.pointSize() + 2)
    app.setFont(font)
    setTheme(Theme.AUTO)
    # Can only retrieve the system accent color on Windows and macOS
    if sys.platform in ["win32", "darwin"]:
        setThemeColor(getSystemAccentColor(), save=False)
        print(getSystemAccentColor().name())
    
    w = Window()
    w.show()
    app.exec()