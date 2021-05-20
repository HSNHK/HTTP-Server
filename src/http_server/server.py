from http_server.middleware import TimeHeader,RequestInformaion
from http_server.url import Path,Redirect,RedirectToFunction
from http_server.response import Response
from http_server.requests import Requests
from http_server.logging import DEBUG
from http_server.logging import Log
from datetime import datetime
import threading
import socket
import sys


class WebServer:
    RouteTableType = list[Path]
    def __init__(self,host="127.0.0.1",port=8080,route=RouteTableType,DEBUG=False,maxConnection=10):
        self.HOST = host
        self.PORT = port
        self.MAXCONNECTION = maxConnection
        self.route_table = route
        self.DEBUG = DEBUG
        self.Middlewares = [TimeHeader,RequestInformaion]
        if self.DEBUG:
            self.Log = Log(Name="Server logging", level=self.DEBUG)
        else:
            self.Log = Log("Server logging")
        
    def __banner(self):
        print("Server is starting up" 
        f"\nHost : {self.HOST}" 
        f"\nPort : {self.PORT}"
        f"\nmax connection : {self.MAXCONNECTION}"
        f"\nNumber of routes : {len(self.route_table)}"
        f"\nAddres : http://{self.HOST}:{self.PORT}"
        f"\ndebug mode : {self.DEBUG}")

    def run(self):
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__banner()
        try:
            self.socket.bind((self.HOST, self.PORT))
            self.Log.info(f"*Start Webserver with http://:{self.HOST}:{self.PORT}")
        except:
            self.Log.critical("Difficult to run. This port is probably reserved")
            self.shutdown()

        self.__listen()

    def shutdown(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        sys.exit(1)

    def __listen(self):
        self.socket.listen(self.MAXCONNECTION)
        try:
            while True:
                (client,address) = self.socket.accept()
                self.Log.info(f"connect new client Host {address[0]} Port {address[1]}")
                threading.Thread(target=self.__handling, args=(client,address)).start()
        except Exception as ex:
            self.Log.error(f"server listen error : {ex}")

    def __handling(self,client: socket.socket,addres: tuple):
        try:
            PACKET_SIZE = 2024
            while True:
                data = client.recv(PACKET_SIZE)

                if not data:
                    break
                request = Requests(data.decode())
                response = Response(client)

                self.Log.info(f"The request {addres[0]}:{addres[1]} {request.method} {request.path} {datetime.now()}")
                isvalid_route = False
                for route in self.route_table:
                    if route.match(request.path):
                        for middleware in self.Middlewares:
                            request,response = middleware(request,response)
                            
                        isvalid_route = True
                        back = route.callback(request, response)
                        if back != None:
                            self.__returnHandling(back, request, response)
                        break

                if isvalid_route == False:
                    self.Log.warning(f"path {request.path} not found !!!")
                    self.not_found(response)
        finally:
            client.close()
        
    def __returnHandling(self,function,request: Requests,response: Response):
        if isinstance(function, Redirect):
            function.go(response)
        elif isinstance(function, RedirectToFunction):
            self.__redirectToFunction(function, request, response)

    def __redirectToFunction(self,function: Redirect,request: Requests,response: Response):
        for path in self.route_table:
            if path.name == function.name:
                path.callback(request, response)

    def not_found(self,response: Response):
        response.notFound()

    def internal_error(self,response: Response):
        response.internalServerError()
