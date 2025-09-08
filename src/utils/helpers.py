import sys
import logging
from datetime import datetime
import os

class CustomException(Exception):
    """A custom exception class that provides detailed error messages
    including the Python script name and line number where the error occurred.
    """
    def __init__(self, errormessage):
        super().__init__(errormessage)
        self.errormessage = errormessage
        
        # Capture error information at initialization time
        _, _, exc_tb = sys.exc_info()
        if exc_tb is not None:
            self.filename = exc_tb.tb_frame.f_code.co_filename
            self.line_number = exc_tb.tb_lineno
        else:
            self.filename = "unknown"
            self.line_number = 0
            
        # Log the exception when it's created
        error_message = f"Error occurred in file: '{self.filename}' at line {self.line_number}: {self.errormessage}"
        logging.error(error_message)
      
    def __str__(self):
        # Format and return the final error message
        return f"Error occurred in file: '{self.filename}' at line {self.line_number}: {self.errormessage}"
    

log_file = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
logs_path = os.path.join(os.getcwd(), "logs")
os.makedirs(logs_path, exist_ok=True)

logs_file_path = os.path.join(logs_path, log_file)

logging.basicConfig(filename=logs_file_path, format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
