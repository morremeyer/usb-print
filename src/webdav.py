import requests
from lxml import objectify

WEBDAV_STATUS_CODE = {
    "OK": 200,
    "CREATED": 201,
    "NO_CONTENT": 204,
    "MULTI_STATUS": 207,
    "NOT_FOUND": 404,
    "METHOD_NOT_ALLOWED": 405,
    "PRECONDITION_FAILED": 412,
    "REQUEST_URI_TOO_LONG": 414,
    "UNPROCESSABLE_ENTITY": 422,
    "LOCKED": 423,
    "FAILED_DEPENDENCY": 424,
    "INSUFFICIENT_STORAGE": 507,
}


class Client:
    def __init__(self, url, username, password):
        self._url = url
        self._session = requests.Session()
        self._session.auth = (username, password)
        self._authenticated = False

    def authenticate(self):
        response = self._session.get(self._url)
        if response.status_code == 200:
            self._authenticated = True
        return self._authenticated

    def send_request(self, verb, path, body="", headers=None, properties=None):
        if not headers:
            headers = {}
        response = self._session.request(verb, path, data=body, headers=headers)
        return response

    def get_request_path(self, path):
        return self._url + path

    def propfind(self, path, properties=None):
        if not self._authenticated:
            self.authenticate()
        verb = "PROPFIND"
        body = self.get_propfind_body()
        requestpath = self.get_request_path(path)
        headers = {"Depth": "1"}
        response = self.send_request(verb, requestpath, body=body, headers=headers)
        if response.status_code == WEBDAV_STATUS_CODE["MULTI_STATUS"]:
            xml_without_encoding_declaration = "\n".join(response.text.split("\n")[1:])
            return objectify.fromstring(xml_without_encoding_declaration)
        print(response.status_code)
        return None

    def get(self, path):
        verb = "GET"
        requestpath = self.get_request_path(path)
        response = self.send_request(verb, requestpath)
        if response.status_code == WEBDAV_STATUS_CODE["OK"]:
            return response.text
        return False

    def move(self, path, destination, overwrite):
        verb = "MOVE"
        requestpath = self.get_request_path(path)
        headers = {
            "Destination": f"{self._url}{destination}",
            "Overwrite": "T" if overwrite else "F",
        }
        response = self.send_request(verb, requestpath, headers=headers)
        if response.status_code != WEBDAV_STATUS_CODE["CREATED"]:
            print(response.status_code)
            return False
        return True

    def put(self, path, filename):
        verb = "PUT"
        requestpath = self.get_request_path(path)
        file = open(filename)
        response = self.send_request(verb, requestpath, file.read())
        if response.status_code in (
            WEBDAV_STATUS_CODE["CREATED"],
            WEBDAV_STATUS_CODE["NO_CONTENT"],
        ):
            return True
        return False

    def delete(self, path):
        verb = "DELETE"
        requestpath = self.get_request_path(path)
        response = self.send_request(verb, requestpath)
        if response.status_code == WEBDAV_STATUS_CODE["NO_CONTENT"]:
            return True
        print(response.status_code)

        return False

    def mkcol(self, path):
        verb = "MKCOL"
        requestpath = self.get_request_path(path)
        response = self.send_request(verb, requestpath)
        if response.status_code == WEBDAV_STATUS_CODE["CREATED"]:
            return True
        print(response.status_code)

        return False

    def get_propfind_body(self, properties=None):
        if not properties:
            properties = []
        body = '<?xml version="1.0" encoding="utf-8" ?>'
        body += '<D:propfind xmlns:D="DAV:">'
        if properties:
            body += "<D:prop>"
            for prop in properties:
                body += "<D:" + prop + "/>"
            body += "</D:prop>"
        else:
            body += "<D:allprop/>"
        body += "</D:propfind>"
        return body
