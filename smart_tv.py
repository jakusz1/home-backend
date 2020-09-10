import asyncio
import json
import requests
import toml

from flask import Response
from common import singleton
from enums import SmartApp
from smart_things import waiter


@singleton
class SmartTv:
    def __init__(self):
        config = toml.load("config.toml")
        self.api_url = config['tv_api_url']
        self.api_key = config['tv_api_key']
        self.device_id = config['tv_device_id']
        self.tv_power = self._get_power()

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

    def _get_power(self):
        resp = requests.get(
            f"https://api.smartthings.com/v1/devices/{self.device_id}/states", 
            headers={"Authorization": f"Bearer {self.api_key}"})
        return resp.json()["main"]["switch"]["value"] == "on"

    def refresh_power(self):
        self.tv_power = self._get_power()

    def switch_power(self):
        self.refresh_power()
        self.set_power(not self.tv_power)
        self.refresh_power()
        return Response(f'{{"state": "{self.tv_power}"}}', status=200, mimetype='application/json')

    def switch_on(self):
        self.set_power(True)

    def switch_off(self):
        self.set_power(False)

    def set_power(self, state):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(waiter(self.api_key, self.device_id, state))
