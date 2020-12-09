import weakref
import logging
import asyncio
import consts
from tornado.options import options
from utils.utils import periodic_callback


class NotifyTimer(object):
    def __init__(self, chat_handler):
        self.logger = logging.getLogger(consts.WEB_HANDLER_LOGGER_NAME)
        self.acquire_input_scheduler = None
        self.close_scheduler = None
        self.chat_handler = weakref.proxy(chat_handler)

    @property
    def logger_extra(self):
        try:
            return self.chat_handler.logger_extra
        except Exception as e:
            return {consts.WEB_HANDLER_EXTRA_KEY: "unknown"}

    def reset(self):
        self.logger.debug("NotifyTimer [%d] reset",
                          id(self),
                          extra=self.logger_extra)
        self.stop_acquire_input_scheduler()
        self.stop_close_scheduler()
        self.acquire_input_scheduler = periodic_callback(
                self.acquire_input, options.acquire_input_interval)
        self.acquire_input_scheduler.start()

    def stop(self):
        self.logger.debug("NotifyTimer [%d] stop",
                          id(self),
                          extra=self.logger_extra)
        self.stop_acquire_input_scheduler()
        self.stop_close_scheduler()

    def stop_acquire_input_scheduler(self):
        if self.acquire_input_scheduler is not None:
            self.acquire_input_scheduler.stop()
            self.acquire_input_scheduler = None

    def stop_close_scheduler(self):
        if self.close_scheduler is not None:
            self.close_scheduler.stop()
            self.close_scheduler = None

    async def acquire_input(self):
        try:
            await self.chat_handler.acquire_input()
            self.stop_acquire_input_scheduler()
            self.close_scheduler = periodic_callback(
                    self.close_chat_handler, options.close_interval)
            self.close_scheduler.start()
            self.logger.info("acquire input success",
                             extra=self.logger_extra)
        except Exception as e:
            self.logger.exception("exception[%s] catched when acquire input",
                                  e, extra=self.logger_extra)
            self.stop()

    async def close_chat_handler(self):
        try:
            await self.chat_handler.timer_close()
            self.stop_close_scheduler()
            self.logger.info("close chat handler success", extra=self.logger_extra)
        except Exception as e:
            self.logger.exception("exception[%s] catched when close chat handler",
                                  e, extra=self.logger_extra)
