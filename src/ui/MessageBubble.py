
from PyQt5.QtWidgets import (
    QFrame, QHBoxLayout, 
    QLabel, QWidget
)
from qfluentwidgets import *
from PyQt5.QtCore import Qt
from qframelesswindow.utils import getSystemAccentColor

class MessageBubble(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)

        self.message_layout = QHBoxLayout(self)
        self.message_layout.setSpacing(12)
        
        self.message_layout.setAlignment(Qt.AlignRight)
        
        message_content = QFrame()
        message_content.setStyleSheet("""
            QFrame {
                border: none;
                background: transparent;
            }
        """)
        message_content_layout = QHBoxLayout(message_content)
        message_content_layout.setContentsMargins(0, 0, 0, 0)
        message_content_layout.setSpacing(0)
        
        text_label = QLabel(text)

        text_label.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.LinksAccessibleByMouse)
       
        text_label.setCursor(Qt.IBeamCursor)

        fm = text_label.fontMetrics()
        text_width = fm.boundingRect(text).width()
        

        if text_width > 400:
            text_label.setWordWrap(True)
            text_label.setMaximumWidth(400)
        else:
            text_label.setWordWrap(False)
            text_label.adjustSize()
            
        if isDarkTheme():
            text_color = "white"
            background_color = "#4B4A4A"
        else:
            text_color = "black"
            background_color = "#D7D6D6"

       
        text_label.setStyleSheet(f"""
            QLabel {{
                background-color: {background_color};
                border-radius: 16px;
                padding: 12px 16px;
                font-size: 14px;
                font-family: 'Segoe UI Variable', 'Segoe UI', sans-serif;
                color: {text_color};
                font-weight: 400;
            }}
        """)
        
        message_content_layout.addWidget(text_label)
        
        self.message_layout.addStretch(1)
        self.message_layout.addWidget(message_content)
    
    def set_style(self, bg_color, text_color):
        """Updates the background AND text color"""
        text_label = self.findChild(QLabel)
        if text_label:
            text_label.setStyleSheet(f"""
                QLabel {{
                    background-color: {bg_color};  /* <--- Dynamic Background */
                    border-radius: 16px;
                    padding: 12px 16px;
                    font-size: 14px;
                    font-family: 'Segoe UI Variable', 'Segoe UI', sans-serif;
                    color: {text_color};          /* <--- Dynamic Text */
                    font-weight: 400;
                }}
            """)