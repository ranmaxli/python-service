import os
from tornado.options import options
import config
config.init()
import logging
import asyncio
import signal
from etornado.application import Application as EApplication
from error_code import ErrorCode, ERROR_INFO_MAP
from etornado.error_code_manager import error_code_manager
from handler_mapping import handler_mapping
import importlib
from etools.elk_record import ElkRecord
from utils.mongo_client import mongo_client


class Application:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.eapp = EApplication()

    def sigint_handler(self, signum):
        self.logger.info("receive signal [%d]", signum)
        asyncio.run_coroutine_threadsafe(self.stop(), asyncio.get_event_loop())

    async def stop(self):
        self.eapp.stop()
        mongo_client.disconnect()

    def run(self):
        self.register_handlers()
        error_code_manager.register_error_enum(ErrorCode, ERROR_INFO_MAP)
        signal.signal(signal.SIGINT, lambda signum, frame: self.sigint_handler(signum))
        self.eapp.run(options.port)

    def register_handlers(self):
        for item in handler_mapping:
            url = item[0]
            cls_path = item[1].split(".")
            module_path = ".".join(cls_path[:-1])
            module = importlib.import_module(module_path)
            cls_name = cls_path[-1]
            cls = getattr(module, cls_name)
            args = item[3] if len(item) > 2 else {}
            self.eapp.register_handler(url, cls, **args)


if __name__ == "__main__":
    app = Application()
    app.run()
