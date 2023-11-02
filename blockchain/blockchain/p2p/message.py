class Message:
    def __init__(self, sender_connector, message_type, data):
        self.sender_connector = sender_connector
        self.message_type = message_type
        self.data = data
