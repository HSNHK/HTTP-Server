from http_server.response import Response
from http_server.requests import Requests
import re

class Path:
    def __init__(self,pattern:str,function,name:str):
        self.pattern = pattern
        self.callback = function
        self.name = name

    def match(self,path:str)->bool:
        if re.match(self.pattern, path):
            return True
        return False
    
class RedirectToFunction:
    def __init__(self,pathName:str):
        self.name = pathName

    def go(self,function,request:Requests,response:Response):
        function(request,response)

class Redirect:
    def __init__(self,pathURL:str):
        self.path = pathURL
        
    def go(self,response:Response):
        response.redirect(self.path)