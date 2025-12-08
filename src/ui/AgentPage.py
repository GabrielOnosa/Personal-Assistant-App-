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

class AgentPage(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)

        # Must set a globally unique object name for the sub-interface
        self.setObjectName(text.replace(' ', '-'))