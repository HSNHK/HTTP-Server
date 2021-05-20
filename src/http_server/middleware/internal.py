from http_server.response import Response
from http_server.requests import Requests
from datetime import datetime


def TimeHeader(request :Requests,response :Response):
    response.headers["time"] = datetime.now()
    return request,response

def RequestInformaion(request: Requests, response: Response):
    print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-\n"
          f"Path : {request.path}\n"
          f"Mathod : {request.method}\n"
          f"Time : {datetime.now()}\n"
          "+-+-+-+-+-+-+-+-+-+-+-+-+-+-")
    return request,response