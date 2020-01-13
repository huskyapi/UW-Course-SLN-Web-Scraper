import logging
import sys

class Logger:
    def __init__(self):
        # Initialize logger object
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # Create external log file
        handler = logging.FileHandler('logs.log')

        # Add formatting so every line includes the time, name and level name
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # Add format handler to logger
        self.logger.addHandler(handler)

        # Enable printing logs to standard output
        self.logger.addHandler(logging.StreamHandler(sys.stdout))


