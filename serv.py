import hcom
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
from tornado.options import define, options


define("port", default=8000, help="runs on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.write({"status_code": status_code, "status_message": self._reason})
        elif status_code == 500:
            self.write({"status_code": status_code, "status_message": "Scraping Error"})

class ErrorHandler(tornado.web.ErrorHandler, IndexHandler):
    pass


class AllTypes(IndexHandler):
    def get(self):
        try:
            self.write({"status_code": 200, "status_message": self._reason, "list": hcom.h_com() + hcom.guide_conf() + hcom.vencity()})
        except:
            raise tornado.web.HTTPError(500)


class hacks(IndexHandler):
    def get(self):
        try:
            self.write({"status_code": 200, "status_message": self._reason, "list": hcom.h_com() + hcom.vencity()})
        except:
            raise tornado.web.HTTPError(500)


class conf(IndexHandler):
    def get(self):
        try:
            self.write({"status_code": 200, "status_message": self._reason, "list": hcom.guide_conf()})
        except:
            raise tornado.web.HTTPError(500)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    settings = {
        'default_handler_class': ErrorHandler,
        'default_handler_args': dict(status_code=404)
    }
    app = tornado.web.Application(
        handlers=[
            (r"/", AllTypes),
            (r"/hackathons", hacks),
            (r"/conferences", conf)
        ], **settings
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
