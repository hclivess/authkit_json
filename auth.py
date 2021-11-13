import tornado.ioloop
import tornado.web
from backend import *


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")


class MainHandler(BaseHandler):
    def get(self):
        if not self.current_user:
            self.render("login.html")
        else:
            name = tornado.escape.xhtml_escape(self.current_user)
            self.write(f"Hello, {name}")


class LoginHandler(BaseHandler):
    def post(self, data):
        name = LoginHandler.get_argument(self, "name")
        password = LoginHandler.get_argument(self, "password")
        # print(name, password)

        if not exists_user(name):
            add_user(name, password)

        if login_validate(name, password):
            self.set_secure_cookie("user", self.get_argument("name"), expires_days=28)
            self.redirect("/")
        else:
            self.render("notfound.html")


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_all_cookies()
        self.redirect("/")


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/login(.*)", LoginHandler),
        (r"/logout", LogoutHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    add_user("testuser", "testpass")

    app.settings["cookie_secret"] = cookie_get()
    app.listen(80)
    tornado.ioloop.IOLoop.current().start()
