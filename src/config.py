import os
import tornado.options
import logging.config

def parse_env_config(env):
    common_conf = tornado.options.options.common_config
    arr = common_conf.split(".")
    arr[-2] += "_%s" % env
    path = ".".join(arr)
    if not os.path.exists(path):
        logger = logging.getLogger("config")
        logger.warning("env config [%s] not exists", path)
        return
    tornado.options.parse_config_file(path)

def define_options():
    tornado.options.define(
        "common_config",
        type=str,
        help="common config file",
        callback=lambda path: tornado.options.parse_config_file(path))
    tornado.options.define(
        "env",
        type=str,
        help="environment, dev|test|online",
        callback=lambda env: parse_env_config(env))
    tornado.options.define("port", type=int, help="server port")
    tornado.options.define("logging_config",
                           type=str,
                           help="logging config file",
                           callback=lambda path: logging.config.fileConfig(path))
    tornado.options.define("heartbeat_close_interval",
                           type=int,
                           help="close websocket connection if do not receive heartbeat"
                                " after [heartbeat_close_interval] seconds")
    tornado.options.define("acquire_input_interval",
                           type=int,
                           help="acquire input if do not receive message"
                                " after [acquire_input_interval] seconds")
    tornado.options.define("close_interval",
                           type=int,
                           help="close connection if do not receive message start"
                                " from acquire input after [close_interval] seconds")
    tornado.options.define("mongo_addr",
                           type=str,
                           help="mongo db address")
    tornado.options.define("mongo_db",
                           type=str,
                           help="mongo database name")
    tornado.options.define("mongo_collection",
                           type=str,
                           help="record collection")

def init():
    tornado.options.options.logging = None
    define_options()
    tornado.options.parse_command_line()
