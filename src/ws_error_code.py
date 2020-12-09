from etools.enum_meta import EnumMeta

class WsErrorCode(metaclass=EnumMeta):
    NONE = 0
    PARSE_MESSAGE_FAILED = 1001
    UNKNOWN_MESSAGE_TYPE = 1002
    HAVE_NOT_YET_INIT = 1003

WS_ERROR_INFO_MAP = {
    WsErrorCode.NONE: "ok",
    WsErrorCode.PARSE_MESSAGE_FAILED: "parse message [{message}] failed",
    WsErrorCode.UNKNOWN_MESSAGE_TYPE: "unknown message type [{message_type}]",
    WsErrorCode.HAVE_NOT_YET_INIT: "have not init yet",
}

class WsErrorCodeException(Exception):

    def __init__(self, error_code, error_info=None):
        if not isinstance(error_code, int):
            raise Exception("error_code [%s] must be int" % error_code)
        if error_info is not None and not isinstance(error_info, dict):
            raise Exception("error_info [%s] must be dict" % error_info)
        self.error_code = error_code
        self.error_info = error_info or {}

    def construct_message(self, message_type, response=None):
        result = {
            "type": message_type,
            "err_no": self.error_code,
            "err_msg": WS_ERROR_INFO_MAP.get(
                self.error_code, "").format(**self.error_info)
        }
        if self.error_code == WsErrorCode.NONE:
            result["response"] = response
        return result

def format_error_info(error_code, kwargs=None):
    kwargs = kwargs or {}
    error_message = WS_ERROR_INFO_MAP.get(error_code, "").format(**kwargs)
    return {"err_no": error_code, "err_msg": error_message}
