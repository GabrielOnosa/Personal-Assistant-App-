from PyQt5.QtCore import  QThread, pyqtSignal
import src.core.LLM_logic as LLM_logic
import traceback 


# am implementat un worked thread pentru a gestiona apeluri catre OpenAI API fara a bloca GUI-ul
class BotWorker(QThread):
    
    finished_signal = pyqtSignal(str)

    def __init__(self, user_text):
        super().__init__()
        self.user_text = user_text

    def run(self):
        try:
            print("Worker thread started")
            
            reply = LLM_logic.get_response(self.user_text)
            
            
            self.finished_signal.emit(reply)
        except Exception:
            error_msg = traceback.format_exc()
            print("Exception in worker:", error_msg)
            self.finished_signal.emit("An error occurred. Please try again.")