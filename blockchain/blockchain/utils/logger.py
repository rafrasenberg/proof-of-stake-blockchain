import json
import logging
from datetime import datetime

from pythonjsonlogger import jsonlogger


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get("timestamp"):
            # this doesn't use record.created, so it is slightly off
            now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            log_record["timestamp"] = now
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname

        # Uvicorn config
        log_record.pop("color_message", None)  # Remove uvicorn color message
        if "http" in record.__dict__:
            log_record["http"] = record.__dict__["http"]


def json_translate(obj):
    from blockchain.p2p.socket_communication import SocketCommunication

    if isinstance(obj, SocketCommunication):
        return {
            "ip": obj.socket_connector.ip,
            "port": obj.socket_connector.port,
        }


# logger = logging.getLogger()
logger = logging.root
logger.setLevel(logging.INFO)
logHandler = logging.StreamHandler()
formatter = CustomJsonFormatter(
    json_default=json_translate, json_encoder=json.JSONEncoder
)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logging.getLogger("uvicorn.access").disabled = True
