from socket import socket
import json

class Response:
    def __init__(self,client:socket):
        self.client=client

        self.headers=dict()
        self.cookies=dict()

        self.__statusCode={
            200: "OK",
            201: "Created",
            202: "Accepted",
            203: "Non-Authoritative Information",
            204: "No Content",
            205: "Reset Content",
            305: "Use Proxy",
            301: "Moved Permanently",
            308: "Permanent Redirect",
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            405: "Method Not Allowed",
            406: "Not Acceptable",
            408: "Request Timeout",
            500: "Internal Server Error",
            501: "Not Implemented",
            502: "Bad Gateway",
            503: "Service Unavailable",
            504: "Gateway Timeout",
            505: "HTTP Version Not Supported"
        }

    def __sendResponse(self,content:str,status:int,contentType:str):
        response_header = f"HTTP/1.1 {status} {contentType}\r\n"
        response_header += f"Server: simple http web Server\r\n"
        response_header += f"Content-Length: {len(content)}\r\n"
        response_header += f"Connection: close\r\n"
        response_header += f"{self.__createHeader}"
        response_header += f"Content-Type: {contentType}\r\n\r\n"

        self.client.send(response_header.encode("utf-8"))
        self.client.send(content.encode("utf-8"))

    @property
    def __createHeader(self)->str:
        if len(self.headers)<1 and len(self.cookies)<1:
            return None

        header_items="\r\n".join(f"{item[0]}:{item[1]}" for item in self.headers.items())

        cookie_items =f"set-cookie:"+";".join(f"{item[0]}={item[1]}" for item in self.cookies.items())

        return f"{header_items}\r\n{cookie_items}\r\n"
    
    def send(self,content:str,statusCode:int,contentType:str):
        self.__sendResponse(content, statusCode, contentType)
    
    def sendJson(self,content:dict,statusCode:int):
        self.__sendResponse(json.dumps(content), statusCode, "application/json")
    
    def sendJsonString(self,content:str,statusCode:int):
        self.__sendResponse(content, statusCode, "application/json")
    
    def redirect(self,path:str):
        self.headers["Location"] = path
        self.__sendResponse("", 308, None)