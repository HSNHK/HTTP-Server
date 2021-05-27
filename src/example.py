from http_server.url import Path,Redirect
from http_server.requests import Requests
from http_server.response import Response
from http_server.server import WebServer


def index(request: Requests,response: Response):
    response.headers["time"] = "12:12"
    response.cookies["name"] = "mywebserver"
    response.sendJson({"name":"HSNHK","age":20}, 200)

def home(request: Requests,response: Response):
    return Redirect("/")

urlpatterns = [
    Path("^\/$", index, name="index"),
    Path("^\/home$", home, name="home")
]

server = WebServer(port=8080, route=urlpatterns)
server.fileServer("/media/","./media")
server.run()
