from socket import socket
import json
import os

class Response:
    def __init__(self,client: socket):
        self.client: socket = client

        self.headers: dict = {}
        self.cookies: dict = {}

        self.BUFFER_SIZE: int = 1024 # send 1024 bytes each time step

        self.__statusCode: dict = {
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

    def __header(self, statusCode: int, contentType: str, length: int) -> str:
        response_header: str = f"HTTP/1.1 {statusCode} {contentType}\r\n"
        response_header += f"Server: simple http web Server\r\n"
        response_header += f"Content-Length: {length}\r\n"
        response_header += f"Connection: close\r\n"
        header: str = self.__createHeader
        response_header += header if header != None else ""
        response_header += f"Content-Type: {contentType}\r\n\r\n"
        return response_header

    def __sendResponse(self, content, status: int, contentType: str):
        response_header = self.__header(status, contentType, len(content))
        self.client.send(response_header.encode("utf-8"))
        if isinstance(content,bytes):
            self.client.send(content)
        else:
            self.client.send(content.encode("utf-8"))

    @property
    def __createHeader(self) -> str:
        if len(self.headers)<1 and len(self.cookies)<1:
            return None

        header_items: str = "\r\n".join(f"{item[0]}:{item[1]}" for item in self.headers.items())

        cookie_items: str = f"set-cookie:"+";".join(f"{item[0]}={item[1]}" for item in self.cookies.items())

        return f"{header_items}\r\n{cookie_items}\r\n"
    
    def send(self,content: str,statusCode: int,contentType: str):
        self.__sendResponse(content, statusCode, contentType)
    
    def sendJson(self,content: dict,statusCode: int):
        self.__sendResponse(json.dumps(content), statusCode, "application/json")
    
    def sendJsonString(self,content: str,statusCode: int):
        self.__sendResponse(content, statusCode, "application/json")
    
    def redirect(self,path: str):
        self.headers["Location"] = path
        self.__sendResponse("", 308, None)

    def sendFile(self,filePath: str,statusCode: int,contentType: str):
        fileSize: bytes = os.path.getsize(filePath)
        if fileSize >= 1000:
            fileSize = fileSize >> 10 # kilobytes (kB)
        elif fileSize >= 1000**2:
            fileSize = fileSize >> 20 # megabyte (MB)
        elif fileSize >= 1000**3:
            fileSize = fileSize >> 30 # gigabyte (GB)
        
        response_header: str = self.__header(statusCode, contentType, fileSize)
        self.client.send(response_header.encode("utf-8"))

        with open(filePath, "rb") as file:
            while True:
                bytes_read = file.read(self.BUFFER_SIZE)
                if not bytes_read:
                    break
                self.client.sendall(bytes_read)
                
    def notFound(self,message="Not Found"):
        self.__sendResponse(f"<h1>{message}</h1>", 404, "text/html")

    def internalServerError(self,message="Internal Server Error"):
        self.__sendResponse(f"<h1>{message}<h1>", 500, "text/html")
