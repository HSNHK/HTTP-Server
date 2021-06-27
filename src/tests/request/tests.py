import sys
sys.path.insert(0, "../../http_server")
from requests import Requests
import unittest
import json


class RequestTests(unittest.TestCase):
    def setUp(self):
        simpleRequest: str = """HTTP/1.x 200 OK\nTransfer-Encoding : chunked
                                Date : Sat, 28 Nov 2009 04:36:25 GMT\nServer : LiteSpeed
                                Connection : close\nX-Powered-By : W3 Total Cache/0.8
                                Pragma : public\nExpires : Sat, 28 Nov 2009 05:36:25 GMT
                                Etag : pub1259380237;gz\nCache-Control : max-age=3600, public
                                Content-Type : text/html; charset=UTF-8\nCookie : PHPSESSID=r2t5uvjq435r4q7ib3vtdjq120
                                Last-Modified : Sat, 28 Nov 2009 03:50:37 GMT\nX-Pingback : https://code.tutsplus.com/xmlrpc.php
                                Content-Encoding : gzip\nVary : Accept-Encoding, Cookie, User-Agent\r\n\r\n{"name":"HSNHK"}
                                """
        self.request = Requests(simpleRequest)
        
    def test_get_cookie(self):
        self.assertEqual(self.request.cookies["PHPSESSID"],"r2t5uvjq435r4q7ib3vtdjq120")

    def test_get_header(self):
        self.assertEqual(self.request.headers["Pragma"],"public")

    def test_body(self):
        self.assertIsInstance(self.request.body, str)
        body = json.dumps(self.request.body)
        self.assertEqual(body["name"],"HSNHK")

if __name__ == "__main__":
    unittest.main()
