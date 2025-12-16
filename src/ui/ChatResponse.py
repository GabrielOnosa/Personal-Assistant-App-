
from PyQt5.QtWidgets import ( QHBoxLayout, QLabel, QWidget)
from qfluentwidgets import *
from PyQt5.QtCore import Qt
class ChatResponse(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        
        self.message_layout = QHBoxLayout(self)
        self.message_layout.setSpacing(12)
        
        
        text_label = QLabel(text)

        if isDarkTheme():
            text_color = "white"
        else:
            text_color = "black"
            

        text_label.setStyleSheet(f"""
                QLabel {{
                    font-size: 14px;
                    font-family: 'Segoe UI Variable', 'Segoe UI', sans-serif;
                    color: {text_color};  
                    font-weight: 425;
                    padding: 5px;
                }}
            """)

        #LLM u trimite multe chestii cu bold, italic links etc. Markdown face ca in loc de **x** sa apara x cu bold de ex 
        text_label.setTextFormat(Qt.MarkdownText)

        text_label.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.LinksAccessibleByMouse)

        text_label.setOpenExternalLinks(True)

        text_label.setCursor(Qt.IBeamCursor)

        text_label.setWordWrap(True)

        self.message_layout.addWidget(text_label)

    def set_text_color(self, color):
        #chatGPT
        text_label = self.findChild(QLabel)
        if text_label:
          
            text_label.setStyleSheet(f"""
                QLabel {{
                    font-size: 14px;
                    font-family: 'Segoe UI Variable', 'Segoe UI', sans-serif;
                    color: {color};  
                    font-weight: 425;
                    padding: 5px;
                }}
            """)
    
        