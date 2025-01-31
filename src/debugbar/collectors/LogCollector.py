from ..messages.Message import Message
import logging

class LogCollector:

    def __init__(self):
        self.messages = []
        self.name = "logging"

    def add_message(self, message, subject=None, options=None):
        self.messages.append(Message(subject, message, options=options))
        return self

    def start_logging(self, log):
        logger = logging.getLogger(log)
        
        logger.addHandler(LogHandler(self))
        return self

    def collect(self):
        collection = []
        info_colors = {
            "INFO": "green",
            "DEBUG": "gray",
            "": "black",
        }
        for message in self.messages:
            collection.append({
                'subject': message.subject,
                'message': message.value,
                'tags': [{
                    'message': message.options.get('level', ''),
                    'color': info_colors[message.options.get('level', '')],
                }],
            })

        print('frrff', collection)

        return {
            'description': "Logging",
            'data': collection,   
        }

class LogHandler(logging.Handler):

    def __init__(self, collector, level=logging.NOTSET):
        super().__init__(level)
        self.collector = collector

    def handle(self, log):
        self.collector.add_message(log.msg, log.name, options={
            "file": log.filename,
            # "time": f"{log.query_time}ms",
            "lineno": log.lineno,
            "logger_name": log.name,
            "level": log.levelname,
        })