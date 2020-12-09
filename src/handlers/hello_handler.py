from etornado.buildin_handlers.base_handler import BaseHandler

class HelloHandler(BaseHandler):

    def do_get(self):
        return "Hello world!"

