
import os
from PyQt5.QtWidgets import (
    QFrame, QHBoxLayout, QApplication, QVBoxLayout, QWidget)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from qfluentwidgets import *
from qfluentwidgets import FluentIcon as FIF
from src.workers.BotWorker import BotWorker
from src.workers.speech_to_text_worker import Speech2TextWorker
from src.ui.MessageBubble import MessageBubble
from src.ui.ChatResponse import ChatResponse
from src.ui.WelcomeWidget import Welcome_Widget
import random
import src.core.LLM_logic as LLM_logic


os.environ["QT_ENABLE_HIGHDPI_SCALING"]   = "1"
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "0.95"
os.environ["QT_SCALE_FACTOR"]             = "0.75"
QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)

        

class MainPage(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        #LLM_logic.clear_conversation()
        self.welcome_texts = [
            "Ready when you are!",
            "How can I assist you today?",
            "Let's chat! What would you like to know?",
            "I'm here to help! Ask me anything.",
            "What can I do for you today?",
            'What are you working on?']
    
        self.initUI()
        self.update_style()
        qconfig.themeChanged.connect(self.update_style)

    def update_style(self):

        if isDarkTheme():
            text_color = "white"
            background_color = "#4B4A4A"
            
        else:
            text_color = "black"
            background_color = "#D7D6D6"

        
        for i in range(self.chat_layout.count()):
            item = self.chat_layout.itemAt(i)
            
            if item:
                widget = item.widget()
                
                if isinstance(widget, ChatResponse):
                    widget.set_text_color(text_color)

                elif isinstance(widget, MessageBubble):
                    widget.set_style(background_color, text_color)    

    def initUI(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.header_layout = QHBoxLayout()
        self.header_layout.setContentsMargins(16, 16, 16, 16)
        self.chat_title = SubtitleLabel("Chat ", self)
        self.new_chat_button = PushButton(FIF.MESSAGE, "New Chat")
        self.header_layout.addWidget(self.chat_title, 1, Qt.AlignLeft | Qt.AlignTop)
        self.header_layout.addWidget(self.new_chat_button, 0, Qt.AlignRight | Qt.AlignTop)
        self.new_chat_button.clicked.connect(self.on_chat_reset)
        layout.addLayout(self.header_layout)

        self.scroll_area = SmoothScrollArea()
        self.scroll_area.setWidgetResizable(True)
        #self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setStyleSheet("background: transparent")
        self.scroll_area.viewport().setStyleSheet("background: transparent")
        self.setObjectName('home-interface')
        
        self.header_layout = QHBoxLayout()

        self.chat_widget = QWidget()
        
        self.chat_layout = QVBoxLayout(self.chat_widget)
        self.chat_layout.setContentsMargins(16, 16, 16, 16)
        self.chat_layout.setSpacing(8)
        self.chat_layout.addStretch()
        self.scroll_area.setWidget(self.chat_widget)
        
        
        
        layout.addWidget(self.scroll_area)
        

        input_container = QWidget()
        
        input_container_layout = QHBoxLayout(input_container)
        input_container_layout.setContentsMargins(16, 12, 16, 12)
        input_container_layout.setSpacing(8)
        
        self.textbox = LineEdit()
        self.textbox.setPlaceholderText(" How can I help ...?")

        self.send_button = ToolButton(FIF.SEND)
        self.microphone_button = ToolButton()
        self.microphone_button.setIcon(FIF.MICROPHONE)
        
        input_container_layout.addWidget(self.textbox)
        input_container_layout.addWidget(self.microphone_button)
        input_container_layout.addWidget(self.send_button)


        layout.addWidget(input_container)
        
        self.send_button.clicked.connect(self.on_send)
        self.microphone_button.clicked.connect(self.speech_to_text)
        self.textbox.returnPressed.connect(self.on_send)


        self.welcome_widget = Welcome_Widget(self.welcome_texts[random.randint(0, len(self.welcome_texts)-1)])
        self.chat_layout.insertStretch(2)
        #self.chat_layout.addSpacing(200)
        self.chat_layout.insertWidget(1, self.welcome_widget)
        self.chat_layout.insertStretch(2)
        
        #self.add_response("👋 Hello! How can I help you today?")
    
    
    def add_message(self, text):
        message = MessageBubble(text)
        self.chat_layout.insertWidget(self.chat_layout.count()-1, message)

    def add_response(self, text):
        message = ChatResponse(text)
        self.chat_layout.insertWidget(self.chat_layout.count()-1, message)
    
    
    def on_send(self):
        text = self.textbox.text().strip()
        if not text:
            InfoBar.warning(
                title="Empty Message",
                content="Please type a message first!",
                parent=self
            )
            return
        
        if getattr(self, "welcome_widget", None):
            self.chat_layout.removeWidget(self.welcome_widget)
            self.welcome_widget.deleteLater()
            self.welcome_widget = None
            for i in range(2):
                self.chat_layout.removeItem(self.chat_layout.itemAt(0))
        
        self.add_message(text)
        self.textbox.clear()

        self.typing_indicator = ChatResponse("Thinking...")
        self.chat_layout.insertWidget(self.chat_layout.count()-1, self.typing_indicator)
        #self.chat_layout.insertWidget(0, self.typing_indicator)

        
        self.send_button.setEnabled(False)
        self.microphone_button.setEnabled(False)
        self.textbox.setEnabled(False)

        self.bot_worker = BotWorker(text)
        self.bot_worker.finished_signal.connect(self.on_bot_response)
        self.bot_worker.start()

        #QTimer.singleShot(100, lambda: self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum()))
        QTimer.singleShot(10, self.scroll_to_bottom_smoothly)

    def scroll_to_bottom_smoothly(self):
            #facut full cu gemini

            scrollbar = self.scroll_area.verticalScrollBar()

            self.anim = QPropertyAnimation(scrollbar, b"value")


            self.anim.setDuration(500)

 
            self.anim.setStartValue(scrollbar.value())
            self.anim.setEndValue(scrollbar.maximum())

            self.anim.setEasingCurve(QEasingCurve.OutCubic)

           
            self.anim.start()
        
        
    def on_bot_response(self, reply):
        
        if getattr(self, "typing_indicator", None):
            self.chat_layout.removeWidget(self.typing_indicator)
            self.typing_indicator.deleteLater() 
            self.typing_indicator = None

     
        self.add_response(reply)

       
        self.send_button.setEnabled(True)
        self.microphone_button.setEnabled(True)
        self.textbox.setEnabled(True)

       
        QTimer.singleShot(10, self.scroll_to_bottom_smoothly)

    def speech_to_text(self):
        self.microphone_button.setEnabled(False)
        self.textbox.setPlaceholderText(" Listening...")
        self.textbox.setEnabled(False)
        self.send_button.setEnabled(False)

        self.speech2text_worker = Speech2TextWorker()
        self.speech2text_worker.finished_signal.connect(self.on_speech_recognized)
        self.speech2text_worker.start()

    def on_speech_recognized(self, recognized_text):
        self.microphone_button.setEnabled(True)
        self.textbox.setEnabled(True)
        self.send_button.setEnabled(True)
        if recognized_text == "":
            InfoBar.warning(
                title="Did you speak?",
                content="Seems like no speech was detected...",
                parent=self
            )
            return
        self.textbox.setText(recognized_text if recognized_text != "" else "")
        self.textbox.setPlaceholderText(" How can I help ...?")
    
    def on_chat_reset(self):
        LLM_logic.clear_conversation()
        while self.chat_layout.count() > 1:
            item = self.chat_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        self.welcome_widget = Welcome_Widget(self.welcome_texts[random.randint(0, len(self.welcome_texts)-1)])
        self.chat_layout.insertStretch(2)
        self.chat_layout.insertWidget(1, self.welcome_widget)
        self.chat_layout.insertStretch(2)
            