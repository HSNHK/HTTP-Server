class Requests:
    def __init__(self,request: str):
        self.__info = request.splitlines()[0].split()

        self.method = self.__info[0]
        self.path = self.__info[1]
        self.version = self.__info[2]

        self.cookies = dict()
        self.headers = dict()

        self.body = str()
        self.__analyzer(request)

    def __analyzer(self,request: str):
        segments = request.split("\r\n\r\n")

        if self.method == "POST" or self.method == "PUT":
            self.body = segments[1]
            
        dataSplited = segments[0].split("\n")
        for item in dataSplited:
            if ":" in item:
                if item.split(":")[0] == "Cookie":
                    self.__cookie(item)
                else:
                    self.__header(item)
               
    def __cookie(self,item: str):
        cookie = item.split(":")
        if ";" in cookie[1]:
            items = cookie[1].split(";")
            for i in items:
                self.cookies[i.split("=")[0].strip()] = i.split("=")[1].strip()
        else:
            self.cookies[cookie[1].split("=")[0].strip()] = cookie[1].split("=")[1].strip()

    def __header(self,item: str):
        header = item.split(":")
        self.headers[header[0].strip()] = header[1].strip()

    def get_header(self, key: str, default: str) -> str:
        if key in self.headers:
            return self.headers[key]
        return default

    def get_cookie(self, key: str, default: str) -> str:
        if key in self.cookies:
            return self.cookies[key]
        return default

    def get_parameter(self,key:str,default: str) -> str:
        if "?" in self.path:
            parameters = self.path.split("?")[1]
            if "&" in parameters:
                args = parameters.split("&")
                for arg in args:
                    if arg.split("=")[0] == key:
                        return arg.split("=")[1]

            elif parameters.split("=")[0] == key:
                return parameters.split("=")[1]
        return default