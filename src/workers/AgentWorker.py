from PyQt5.QtCore import QThread, pyqtSignal
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from src.core.Agent_logic import graph
import re

class AgentWorker(QThread):
    response_signal = pyqtSignal(str)  
    image_signal = pyqtSignal(str)     
    error_signal = pyqtSignal(str)     
    finished_signal = pyqtSignal()     
    draft_ready_signal = pyqtSignal(str, str)
    
    def __init__(self, user_input: str, thread_id: str = "agent_session"):
        super().__init__()
        self.user_input = user_input
        self.thread_id = thread_id
        self.config = {"configurable": {"thread_id": thread_id}}
        self.image_path = None
        self.draft_text = None

    def get_text_content(self, content) -> str:
        """Extract text from content (handles both str and list)"""
        if content is None:
            return ""
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            text_parts = []
            for block in content:
                if isinstance(block, str):
                    text_parts.append(block)
                elif isinstance(block, dict) and block.get('type') == 'text':
                    text_parts.append(block.get('text', ''))
            return "\n".join(text_parts)
        return str(content)
    
    def quote_extraction(self, message: str) -> str:
        return re.findall('"([^"]*)"', message)[0] if re.findall('"([^"]*)"', message) else message  #extract tesxt within quotes


    def run(self):
        try:
            messages = [HumanMessage(content=self.user_input)]
            
            for event in graph.stream({"messages": messages}, self.config, stream_mode="values"):
                msg = event["messages"][-1]
                
             
                if isinstance(msg, AIMessage):
                    
                    has_tool_calls = hasattr(msg, 'tool_calls') and msg.tool_calls
                    content = self.get_text_content(msg.content)

                    if content.strip():
                        self.response_signal.emit(content.strip())

                    if content.strip() and not has_tool_calls:
                        self.draft_text = content.strip()
        
 
                if isinstance(msg, ToolMessage):
                    content = self.get_text_content(msg.content)
                    if "temp_imagen_image.png" in content:
                        self.image_path = "temp_imagen_image.png"
                        self.image_signal.emit(self.image_path)
                        

            if self.draft_text and self.image_path:
                self.draft_text = self.quote_extraction(self.draft_text)
                self.draft_ready_signal.emit(self.draft_text, self.image_path)
                    
        except Exception as e:
            self.error_signal.emit(f"Error: {str(e)}")
        finally:
            self.finished_signal.emit()