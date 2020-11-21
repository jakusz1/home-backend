import requests
import toml

from common import singleton
from enums import SmartApp


@singleton
class SmartTv:
    def __init__(self):
        config = toml.load("config.toml")
        self.api_url = config['tv_api_url']
        self.api_key = config['tv_api_key']
        self.device_id = config['tv_device_id']
        self.tv_power = False
        self.visible_app = None
        self.update()

    def _get_app_status_by_id(self, app_id):
        return requests.request("GET", f"{self.api_url}/{app_id}")

    def _set_app_off_by_id(self, app_id):
        return requests.request("DELETE", f"{self.api_url}/{app_id}")

    def get_app_status(self, app_name):
        app_id = SmartApp[app_name.upper()].value
        return self._get_app_status_by_id(app_id)

    def set_app_on(self, app_name):
        app_id = SmartApp[app_name.upper()].value
        self.visible_app = SmartApp[app_name.upper()]
        return requests.request("POST", f"{self.api_url}/{app_id}")

    def set_app_off(self, app_name):
        app_id = SmartApp[app_name.upper()].value
        return requests.request("DELETE", f"{self.api_url}/{app_id}")

    def set_all_apps_off(self):
        status_code = 200
        for app in SmartApp:
            if self._set_app_off_by_id(app.value).status_code != 200:
                status_code = 500
        if status_code == 200:
            self.visible_app = None
        return status_code

    def _get_power(self):
        resp = requests.get(
            f"https://api.smartthings.com/v1/devices/{self.device_id}/states",
            headers={"Authorization": f"Bearer {self.api_key}"})
        return resp.json()["main"]["switch"]["value"] == "on"

    def update(self):
        self.tv_power = self._get_power()
        v_app = None
        if self.tv_power:
            for app in SmartApp:
                if self._get_app_status_by_id(app.value).json()["visible"]:
                    v_app = app
        self.visible_app = v_app

    def get_info(self):
        return {
            "power": self.tv_power,
            "visible_app": self.visible_app.name.lower() if self.visible_app else None
        }
