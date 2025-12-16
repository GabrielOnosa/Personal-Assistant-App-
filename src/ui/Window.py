
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, QSize
from qfluentwidgets import *
from qfluentwidgets import FluentIcon as FIF
from src.ui.SettingsPage import SettingsPage
from src.ui.MainPage import MainPage
from src.ui.ChatHistory import ChatHistoryPage
from src.ui.AgentPage import AgentPage



# cod luat mot a mot din documentatie 
class Window(FluentWindow):
    """ Main Interface """

    def __init__(self):
        super().__init__()

        # Create sub-interfaces, when actually using, replace Widget with your own sub-interface 
        self.homeInterface = MainPage(self)
        self.settingInterface = SettingsPage(self)
        #self.ChatHistoryPage = ChatHistoryPage('Chat history', self)
        self.splashScreen = SplashScreen(QIcon('src/ui/assets/Dark_mode_logo.png'), self)
        self.splashScreen.setIconSize(QSize(128, 128))
        self.AgentPage = AgentPage('Agent Mode', self)

        self.initNavigation()
        self.initWindow()
        QTimer.singleShot(650, lambda : self.splashScreen.finish()) #asta am incercat eu - are un effect prea brusc

        qconfig.themeChanged.connect(self.update_window_icon) #asta leaga schimbarea temei de schimbarea iconitei - schimbarea temei e ceva din sistem pyqt shit


    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.CHAT, 'Chat')
        #self.addSubInterface(self.ChatHistoryPage, FIF.HISTORY, 'Chat History')
        #self.navigationInterface.addSeparator()
        self.addSubInterface(self.AgentPage, FIF.ROBOT, 'Agent Mode')
        self.navigationInterface.addSeparator()
        self.addSubInterface(self.settingInterface, FIF.SETTING, 'Settings', NavigationItemPosition.BOTTOM)

    def initWindow(self):

        self.setWindowIcon(QIcon('src/ui/assets/Dark_mode_logo.ico'))
        self.setWindowTitle('Personal Assistant')

    def update_window_icon(self): #vreau sa schimbe iconita in functie de tema
        if isDarkTheme():
            icon_path = 'src/ui/assets/Dark_mode_logo.ico'   
        else:
            icon_path = 'src/ui/assets/Light_mode_logo.ico'  

        self.setWindowIcon(QIcon(icon_path))
        