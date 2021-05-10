# HTTP Server
An example of a http server implementation in Python<br>
This project can also be a very small framework

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

request.get_parameter(key, default)
request.get_header(key, default)
request.get_cookie(key, default)
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
