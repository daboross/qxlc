import json

import requests
from requests.auth import HTTPBasicAuth

HOST = "https://api.pushbullet.com/v2/"


class PushBullet():
    def __init__(self, api_key):
        self.api_key = api_key
        self._headers = {"Accept": "application/json", "Content-type": "application/json",
                         "User-Agent": "qxlc (http://qx.lc)"}
        self._args = {'headers': self._headers, 'auth': HTTPBasicAuth(self.api_key, ""), 'verify': True}

    def push_note(self, title, body, device=None):
        data = {'type': "note", 'title': title, 'body': body}
        if device:
            data["device_iden"] = device
        r = requests.post(HOST + "pushes", json.dumps(data), **self._args)
        return r

    def push_address(self, name, address, device=None):
        data = {'type': 'address', 'name': name, 'address': address}
        if device:
            data["device_iden"] = device
        r = requests.post(HOST + "pushes", json.dumps(data), **self._args)
        return r.json()

    def push_list(self, title, items, device=None):
        data = {'type': 'list', 'title': title, 'items': items}
        if device:
            data["device_iden"] = device
        r = requests.post(HOST + "pushes", json.dumps(data), **self._args)
        return r.json()

    def push_link(self, title, url, device=None):
        data = {'type': 'link', 'title': title, 'url': url}
        if device:
            data["device_iden"] = device
        r = requests.post(HOST + "pushes", json.dumps(data), **self._args)
        return r.json()

    def push_file(self, device, filepath):
        data = {'type': 'file'}
        if device:
            data["device_iden"] = device
        with open(filepath, "rb") as f:
            r = requests.post(HOST + "pushes", json.dumps(data), files=[f], **self._args)

        return r.json()
