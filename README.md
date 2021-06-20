# HTTP Server [![HSNHK - HTTP-Server](https://img.shields.io/static/v1?label=HSNHK&message=HTTP-Server&color=blue&logo=github)](https://github.com/HSNHK/HTTP-Server)
[![stars - HTTP-Server](https://img.shields.io/github/stars/HSNHK/HTTP-Server?style=social)](https://github.com/HSNHK/HTTP-Server)
[![forks - HTTP-Server](https://img.shields.io/github/forks/HSNHK/HTTP-Server?style=social)](https://github.com/HSNHK/HTTP-Server)
[![GitHub release](https://img.shields.io/github/release/HSNHK/HTTP-Server?include_prereleases=&sort=semver)](https://github.com/HSNHK/HTTP-Server/releases/)
[![License](https://img.shields.io/badge/License-_GPL--3.0_License-blue)](#license)
[![issues - HTTP-Server](https://img.shields.io/github/issues/HSNHK/HTTP-Server)](https://github.com/HSNHK/HTTP-Server/issues)

An example of a http server implementation in Python.<br>
This project can also be a very small framework.

# life cycle
```
--------------------------------------------------
| request                             reponse    |
|    |                                   |       |
|    |                                   |       |
|  Accept                              Close     |
|    |            life cycle             |       |
|    |                                   |       |
|  Parse                                Send     |
|    |                                   |       |
|    |                                   |       |
|  Worker -------------------------- Dispatcher  |
--------------------------------------------------
```
# example
```python
def index(request:Requests,response:Response):
    response.send("hello world !", 200, "text/html")

urlpatterns = [
    Path("^\/$", index, name="index"),
 ]

server=WebServer(port=8080,route=urlpatterns)
server.run()
```
# request
Request information
```python
request.method
request.path
request.version
```
Header & Cookie
```python
request.headers
request.cookies 

request.get_header(key, default)
request.get_cookie(key, default)
```
URL
```python
request.get_parameter(key, default)
```
Body
```python
request.body
```
# response
Header & Cookie
```python
response.headers
response.cookies
```
Client Connection
```python
response.client
```
Response
```python
response.send(content, status Code, content Type)
response.sendJson(content, status Code)
response.sendJsonString(content, status Code)
```
Redirect
```python
from http_server.url import Redirect 
...
return Redirect("path")
```
# server
Middleware
```python
def Referer(request: Requests,response: Response):
    if "Referer" in request.headers:
        print(request.headers["Referer"])
    return request,response

server = WebServer(port=8080, route=urlpatterns)
server.Middlewares.append(Referer)
server.run()
```
File Server
```python
server.fileServer(URL, Folder path)
#example
server.fileServer("/media/","./media")
```
## License
Released under [ GPL-3.0 License](/LICENSE) by [@HSNHK](https://github.com/HSNHK).
