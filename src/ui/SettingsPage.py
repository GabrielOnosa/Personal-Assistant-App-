
from PyQt5.QtWidgets import (
    QFrame, QHBoxLayout, QVBoxLayout
)
from PyQt5.QtCore import Qt
from qfluentwidgets import *
import src.core.LLM_logic as LLM_logic


class SettingsPage(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('Settings-Page')
        
        # Create header shit where it will sit
        self.MainLayout = QVBoxLayout(self)
        self.header = QHBoxLayout()
        self.header.setContentsMargins(16, 16, 16, 16)
        # Create header itself
        self.headerLabel = SubtitleLabel('Settings', self)
        
        if isDarkTheme():
            colour = 'white'
        else:
            colour = 'black'
        self.headerLabel.setStyleSheet(f"""
            SubtitleLabel {{
                color: {colour};
            }}
        """)

        self.header.addWidget(self.headerLabel, 0, Qt.AlignLeft | Qt.AlignTop)

        #Declare the actual buttons and stuff
        self.personality_button = ComboBoxSettingCard(configItem = LLM_logic.options.change_personality, icon = FluentIcon.ROBOT, title = 'Personality', content = "Adjust your chatbot's personality. This doesn't affect the quality of the information provided. ", texts = LLM_logic.personalities)
        self.temperature_button = RangeSettingCard(configItem = LLM_logic.options.temperature, icon = FluentIcon.CALORIES, title = 'Temperature', content = "Adjust your chatbot's temperature. This makes the bot more or less creative ")
        self.top_p_button = RangeSettingCard(configItem = LLM_logic.options.top_p, icon = FluentIcon.UP, title = 'Top P', content = "Controls how many word choices are considered. Low is focused; High is diverse.")
        self.theme_mode_button = ComboBoxSettingCard(configItem = LLM_logic.options.theme_mode, icon = FluentIcon.BRUSH, title = 'Theme', content = "Adjust the application theme", texts = ['Light', 'Dark', 'System'])
        self.theme_mode_button.configItem.valueChanged.connect(self.on_theme_changed)
        self.personality_button.configItem.valueChanged.connect(LLM_logic.change_personality)
        
        self.MainLayout.addLayout(self.header)
        self.MainLayout.addWidget(self.personality_button)
        self.MainLayout.addWidget(self.theme_mode_button)

        self.MainLayout.addSpacing(16)

        #RAG add knowledge button
        self.RAG_header = SubtitleLabel('RAG settings for your assistant', self)
        font = self.RAG_header.font()
        font.setPointSize(10)
        self.RAG_header.setFont(font)
        self.RAG_header_box = QHBoxLayout()
        self.rag_file_card = PushSettingCard(
            text = 'Add File',
            icon = FluentIcon.DOCUMENT,
            title = 'Add Knowledge',
            content = 'Add files such as PDFs or txt documents to enhance the assistant\'s knowledge.',
        )
        self.RAG_header_box.addWidget(self.RAG_header, 0, Qt.AlignLeft | Qt.AlignTop) 
        self.RAG_header_box.setContentsMargins(6, 6, 2, 2)
        self.MainLayout.addLayout(self.RAG_header_box)
        self.MainLayout.addWidget(self.rag_file_card)
        

        self.MainLayout.addSpacing(16)
        self.advanced_layout = QHBoxLayout()
        self.advanced_header = SubtitleLabel('Advanced LLM settings meant for fine-tuning your user experience', self)

        font = self.advanced_header.font()
        font.setPointSize(10)
        self.advanced_header.setFont(font)

        self.advanced_layout.addWidget(self.advanced_header, 0, Qt.AlignLeft | Qt.AlignTop)
        self.advanced_layout.setContentsMargins(6, 6, 2, 2)
        self.MainLayout.addLayout(self.advanced_layout)
        self.MainLayout.addWidget(self.temperature_button)
        self.MainLayout.addWidget(self.top_p_button)
        self.MainLayout.addStretch()

    def on_theme_changed(self, value):
        if value == 'Light':
           setTheme(Theme.LIGHT)
        elif value == 'Dark':
            setTheme(Theme.DARK)