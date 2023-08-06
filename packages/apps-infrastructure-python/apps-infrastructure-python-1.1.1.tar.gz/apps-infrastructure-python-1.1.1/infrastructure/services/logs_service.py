import logging
import os


class LogsService:
    def __init__(self, log_path: str = ""):
        self.logs_file_path = "{0}/logs.log".format(log_path)
        if not os.path.exists(self.logs_file_path):
            os.makedirs(os.path.dirname(self.logs_file_path))

        log_formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger()

        file_handler = logging.FileHandler(self.logs_file_path)
        file_handler.setFormatter(log_formatter)
        self.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        self.logger.addHandler(console_handler)
        return

    def logs(self):
        cwd = os.getcwd()
        return open(cwd + "/" + self.logs_file_path, "rt").read()




