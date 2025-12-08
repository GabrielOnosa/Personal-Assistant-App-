from PyQt5.QtCore import  QThread, pyqtSignal
import src.core.LLM_logic as LLM_logic
import traceback 
from src.services.ingestion import ingest


class IngestionWorker(QThread):
    
    finished_signal = pyqtSignal(str)

    def __init__(self, pdf_path):
        super().__init__()
        self.pdf_path = pdf_path

    def run(self):
        try:
            print("Ingestion Worker thread started")
            
            ingest(pdf_path=self.pdf_path)
            
            self.finished_signal.emit("Ingestion completed successfully.")
        except Exception:
            error_msg = traceback.format_exc()
            print("Exception in ingestion worker:", error_msg)
            self.finished_signal.emit("An error occurred during ingestion.")