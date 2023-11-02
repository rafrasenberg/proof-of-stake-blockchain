import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class CustomLogger:
    def __init__(self, level, socket_communication=None):
        global logging
        self.logging = logging
        self.level = level
        self.socket_communication = socket_communication

    def log(self, message):
        logger = None
        message = self.construct_base_message(message)
        if self.level.lower() == "info":
            if self.socket_communication:
                message = message | self.construct_node_info(self.socket_communication)
            logger = self.logging.info(message)

        elif self.level.lower() == "error":
            if self.socket_communication:
                message = message | self.construct_node_info(self.socket_communication)
            logger = self.logging.error(message)
        return logger

    def construct_base_message(self, message):
        return {"message": message}

    def construct_node_info(self, socket_communication):
        return {
            "whoami": {
                "ip": socket_communication.socket_connector.ip,
                "port": socket_communication.socket_connector.port,
            }
        }
