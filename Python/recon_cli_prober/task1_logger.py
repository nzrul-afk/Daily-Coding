import logging
import os
class SecurityLogger:
    def __init__(self, verbose=True):
        self.name="SecurityLogger"
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.log_file = os.path.join(base_dir, "recon.log")
        self.verbose= verbose
        self.logger=logging.getLogger(self.name)
        if self.verbose:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)
    def handler(self):
        log_format = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
        format_handler=logging.Formatter(fmt=log_format, datefmt="%H:%M:%S")
        console_handler=logging.StreamHandler()
        console_handler.setFormatter(format_handler)
        format_handler2=logging.Formatter(fmt=log_format, datefmt="%Y-%m-%d %H:%M:%S")
        file_handler=logging.FileHandler(self.log_file)
        file_handler.setFormatter(format_handler2)
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def debug(self, pesan):
        self.logger.debug(pesan)
    def info(self, pesan):
        self.logger.info(pesan)
    def warning(self, pesan):
        self.logger.warning(pesan)
    def critical(self, pesan):
        self.logger.critical(pesan)
    def error(self, pesan):
        self.logger.error(pesan)
if __name__  == "__main__":
    log = SecurityLogger(verbose=False)
    log.handler()
    log.debug("Ini pesan debug")
    log.info("Server berhasil dinyalakan")
    log.warning("Ada ip mencurigakan")
    log.error("Koneksi gagal")
    log.critical("Database jebol")

