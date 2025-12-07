from PyQt5.QtCore import  QThread, pyqtSignal
from src.services.s_to_text import transcribe_from_microphone
import traceback 



# aici e un worker care gestioneaza speech_to_text-ul in background fara sa blochez interfata

class Speech2TextWorker(QThread):
    finished_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
    
    def run(self):
        try:
            print("Speech to text worker started")
            
            text = transcribe_from_microphone()
            
            #
            self.finished_signal.emit(text)
        except Exception:
            error_msg = traceback.format_exc()
            print("Exception in speech to text worker:", error_msg)
            self.finished_signal.emit("")