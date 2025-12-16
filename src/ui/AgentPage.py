
from PyQt5.QtWidgets import (
    QFrame, QHBoxLayout, QVBoxLayout, QWidget, QSplitter, QLabel, QSizePolicy)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer
from qfluentwidgets import *
from qfluentwidgets import FluentIcon as FIF
from src.workers.speech_to_text_worker import Speech2TextWorker
from src.ui.MessageBubble import MessageBubble
from src.ui.ChatResponse import ChatResponse
from src.workers.AgentWorker import AgentWorker

from qframelesswindow.utils import getSystemAccentColor


class AgentPage(QFrame):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.agent_worker = None
        self.current_image_path = None
        self.current_draft_text = None
        self.awaiting_confirmation = False
        self.session_thread_id = "agent_session_1"
        self.setObjectName(text.replace(' ', '-'))
        
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

      
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setHandleWidth(2) 
    
        self.splitter.setChildrenCollapsible(False) 

        # Left SIDE
        self.chat_container = QWidget()
        self.chat_layout_structure = QVBoxLayout(self.chat_container)
        self.chat_layout_structure.setContentsMargins(0, 0, 0, 0)
        
        # Header
        self.header_layout = QHBoxLayout()
        self.header_layout.setContentsMargins(16, 16, 16, 16)
        self.chat_title = SubtitleLabel("Twitter Agent", self)
        self.header_layout.addWidget(self.chat_title, 1, Qt.AlignLeft | Qt.AlignTop)
        self.chat_layout_structure.addLayout(self.header_layout)

        # Chat Scroll Area
        self.scroll_area = SmoothScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("background: transparent; border: none;")
        
        self.scroll_widget = QWidget()
        self.msg_layout = QVBoxLayout(self.scroll_widget)
        self.msg_layout.setContentsMargins(16, 16, 16, 16)
        self.msg_layout.setSpacing(16)
        self.msg_layout.addStretch() 
        
        self.scroll_area.setWidget(self.scroll_widget)
        self.chat_layout_structure.addWidget(self.scroll_area)

        # Input Area
        self.input_container = QWidget()
        self.input_layout = QHBoxLayout(self.input_container)
        self.input_layout.setContentsMargins(16, 12, 16, 12)
        self.input_layout.setSpacing(8)
        

        self.textbox = LineEdit()
        self.textbox.setPlaceholderText("Tell me what to post...")
        self.textbox.returnPressed.connect(self.on_send)
        
        self.send_button = ToolButton(FIF.SEND)
        self.send_button.clicked.connect(self.on_send)
        
        self.input_layout.addWidget(self.textbox)
        self.input_layout.addWidget(self.send_button)
        self.chat_layout_structure.addWidget(self.input_container)

        #RIGHT SIDE
        self.preview_scroll = SmoothScrollArea()
        self.preview_scroll.setWidgetResizable(True)
        self.preview_scroll.setStyleSheet("background: transparent; border: none;")
        
    
        self.preview_container = QWidget()
        self.preview_container.setObjectName("PreviewFrame")
        
  
        self.preview_layout = QVBoxLayout(self.preview_container)
        self.preview_layout.setAlignment(Qt.AlignTop)
        self.preview_layout.setContentsMargins(20, 40, 20, 20)
        self.preview_layout.setSpacing(15)
        
  
        self.preview_label = QLabel("Your post draft will appear here... The image below is placeholder")
        self.preview_label.setWordWrap(True)

        self.preview_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        self.preview_label.setStyleSheet("""
            QLabel {
                font-size: 15px;
                font-family: 'Segoe UI', sans-serif;
                color: white;
                padding: 5px;
            }
        """)
        self.preview_layout.addWidget(self.preview_label)
        
        # 6. Image Slot
        self.post_image = QLabel()
        self.post_image.setAlignment(Qt.AlignCenter)
        self.post_image.setPixmap(QPixmap('src/ui/assets/image.jpg').scaled(500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.preview_layout.addWidget(self.post_image)

        self.preview_layout.addSpacing(20)

        # 7. Buttons
        self.actions_layout = QHBoxLayout()
        #self.post_btn = PrimaryPushButton(FIF.SEND, "Post Now")
        
        #self.actions_layout.addWidget(self.post_btn)
        
        self.preview_layout.addLayout(self.actions_layout)
        self.preview_layout.addStretch() 

        self.preview_scroll.setWidget(self.preview_container)

   
        self.splitter.addWidget(self.chat_container)
        self.splitter.addWidget(self.preview_scroll) 
        
        self.main_layout.addWidget(self.splitter)
        
   
        accent_color = getSystemAccentColor().name()


        self.splitter.setStyleSheet(f"""
            QSplitter::handle {{
                background-color: #4B4A4A;
            }}
            QSplitter::handle:pressed {{
                background-color: {accent_color}; 
            }}
        """)
        QTimer.singleShot(0, self.center_splitter)


    def center_splitter(self):
        w = self.splitter.width()
        half = w // 2
        self.splitter.setSizes([half, half])

    def on_send(self):
        user_text = self.textbox.text().strip()
        if not user_text:
            InfoBar.warning(
                title="Empty Message",
                content="Please type a message first!",
                parent=self
            )
            return
        
        # Add user message to chat
        self.add_chat_message(user_text)
        self.textbox.clear()
        
        # Disable send button while processing
        self.send_button.setEnabled(False)
        #self.post_btn.setEnabled(False)
        self.awaiting_confirmation = False
        
        # Start agent worker
        self.agent_worker = AgentWorker(user_text, self.session_thread_id)
        self.agent_worker.response_signal.connect(self.on_agent_response)
        self.agent_worker.image_signal.connect(self.on_image_generated)
        self.agent_worker.error_signal.connect(self.on_agent_error)
        self.agent_worker.draft_ready_signal.connect(self.on_draft_ready)
        self.agent_worker.start()
    
    def on_agent_response(self, text: str):
        #self.preview_label.setText(text)
        self.add_response(text)
        #self.draft_text.setText(text)
        #self.add_chat_message(text)
    
    def on_image_generated(self, image_path: str):
        if image_path != "Generating image...":
            self.current_image_path = image_path
            # pixmap = QPixmap(image_path)
            # if not pixmap.isNull():
            #     scaled_pixmap = pixmap.scaled(500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            #     self.post_image.setPixmap(scaled_pixmap)
            #     #self.post_btn.setEnabled(True)
            #     self.awaiting_confirmation = True
    def on_draft_ready(self, draft_text: str, image_path: str):
        """Called when both draft text and image are ready"""
        self.current_draft_text = draft_text
        self.current_image_path = image_path
        self.awaiting_confirmation = True
        
        # Update preview panel (right side)
        self.preview_label.setText(f"{draft_text}\n\n")
        
        # Show the image
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.post_image.setPixmap(scaled_pixmap)
            self.post_image.show()
        
        # Show the post button
        #self.post_btn.show()



    def on_agent_error(self, error: str):
        InfoBar.error(
                title="Agent Error",
                content="An error occurred while processing your request. Error: " + error,
                parent=self,
                duration= 3000
            )
    
    def on_agent_finished(self):
        self.send_button.setEnabled(True)
    
    def on_confirm_post(self):
        if not self.awaiting_confirmation:
            return
        
        # Send confirmation to agent
        self.textbox.setText("Yes, post it!")
        #self.post_btn.setEnabled(False)
        
        self.send_button.setEnabled(False)
        self.agent_worker = AgentWorker("Yes, post it!", self.session_thread_id)
        self.agent_worker.response_signal.connect(self.on_post_confirmed)
        self.agent_worker.finished_signal.connect(self.on_agent_finished)
        self.agent_worker.start()
    
    def on_post_confirmed(self, text: str):
        if "Successfully posted tweet" in text:
            InfoBar.success(
                title="Success",
                content="Your post has been successfully published!",
                parent=self
            )
            self.textbox.clear()
            self.awaiting_confirmation = False
        else:
            self.add_response(text)
    
    def add_chat_message(self, text: str):
        bubble = MessageBubble(text)
        self.msg_layout.insertWidget(self.msg_layout.count() - 1, bubble)

    def add_response(self, text: str):
        response = ChatResponse(text)
        self.msg_layout.insertWidget(self.msg_layout.count() - 1, response)
        