import json
import requests
import toml

from flask import Response
from common import singleton
from enums import SmartApp


@singleton
class SmartTv:
    def __init__(self):
        self.api_url = toml.load("config.toml")['tv_api_url']

    def _get_app_status_by_id(self, app_id):
        return requests.request("GET", f"{self.api_url}/{app_id}")

    def _set_app_off_by_id(self, app_id):
        return requests.request("DELETE", f"{self.api_url}/{app_id}")

    def get_app_status(self, app_name):
        app_id = SmartApp[app_name.upper()].value
        return self._get_app_status_by_id(app_id)

    def set_app_on(self, app_name):
        app_id = SmartApp[app_name.upper()].value
        return requests.request("POST", f"{self.api_url}/{app_id}")

    def set_app_off(self, app_name):
        app_id = SmartApp[app_name.upper()].value
        return requests.request("DELETE", f"{self.api_url}/{app_id}")

    def set_all_apps_off(self):
        status_code = 200
        for app in SmartApp:
            if self._set_app_off_by_id(app.value).status_code != 200:
                status_code = 500
        return Response(status=status_code, mimetype='application/json')
