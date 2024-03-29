import asyncio
import json
from time import sleep
from traceback import format_exc

from flask import Flask, request, Response, send_file

import smart_things
from ir_denon import IrDenon
from light_repository import LightRepository
from smart_tv import SmartTv
from spotify_helper import SpotifyHelper, SpotiLightException


loop = asyncio.get_event_loop()
app = Flask(__name__,
            static_url_path='',
            static_folder='web')


@app.route('/', methods=['GET'])
def get_frontend():
    return send_file("web/index.html")


@app.route('/api/v2/spotify', methods=['GET'])
def get_spotify():
    try:
        return Response(f'{{"best_rgb": {str(SpotifyHelper().get_color_from_currently_played_album())}}}',
                        status=200,
                        mimetype='application/json')
    except (SpotiLightException, AttributeError) as error:
        return Response(f'{{"error": "{repr(error)}", "traceback": "{format_exc()}"}}', status=500,
                        mimetype='application/json')


@app.route('/api/v2/spotify/album', methods=['GET'])
def get_spotify_album():
    return Response(SpotifyHelper().current_album, status=200, mimetype='image/jpeg')


@app.route('/api/v2/denon', methods=['GET'])
def get_denon():
    return Response(json.dumps(IrDenon().get_info()), status=200, mimetype='application/json')


@app.route('/api/v2/denon/<action>', methods=['POST'])
def action_denon(action):
    try:
        IrDenon().send(action, request.json['count'])
        return Response(json.dumps(IrDenon().get_info()), status=200, mimetype='application/json')
    except Exception as error:
        return Response(f'{{"error": "{repr(error)}", "traceback": "{format_exc()}"}}', status=500,
                        mimetype='application/json')


@app.route('/api/v2/tv/power/<action>', methods=['POST'])
def set_tv(action):
    tv = SmartTv()
    if action == 'switch':
        tv.update()
        loop.run_until_complete(smart_things.waiter(tv.api_key, tv.device_id, not tv.tv_power))
        sleep(5)
        tv.update()
        return Response(json.dumps(tv.get_info()), status=200, mimetype='application/json')
    elif action == 'on':
        loop.run_until_complete(smart_things.waiter(tv.api_key, tv.device_id, True))
        sleep(5)
        tv.update()
        return Response(json.dumps(tv.get_info()), status=200, mimetype='application/json')
    elif action == 'off':
        loop.run_until_complete(smart_things.waiter(tv.api_key, tv.device_id, False))
        tv.tv_power = False
        return Response(json.dumps(tv.get_info()), status=200, mimetype='application/json')
    else:
        return Response(status=400, mimetype='application/json')


@app.route('/api/v2/tv/apps', methods=['DELETE'])
def smart_tv_apps():
    return Response(status=SmartTv().set_all_apps_off(), mimetype='application/json')


@app.route('/api/v2/tv', methods=['GET'])
def get_tv():
    SmartTv().update()
    return Response(json.dumps(SmartTv().get_info()), status=200, mimetype='application/json')


@app.route('/api/v2/tv/apps/<app_name>/<action>', methods=['POST'])
def smart_tv_app(app_name, action):
    if action == 'on':
        if app_name == 'pc':
            SmartTv().set_all_apps_off()
        else:
            SmartTv().set_app_on(app_name)
        return Response(json.dumps(SmartTv().get_info()), status=200, mimetype='application/json')
    elif action == 'off':
        SmartTv().set_app_off(app_name)
        return Response(json.dumps(SmartTv().get_info()), status=200, mimetype='application/json')
    else:
        return Response(status=400, mimetype='application/json')


@app.route('/api/v2/lights/<light_name>/<action>', methods=['POST'])
def action_light(light_name, action):
    light = LightRepository().get_light_by_name(light_name)
    if not light:
        return Response(status=404, mimetype='application/json')
    try:
        if action == "switch":
            light.switch_power()
        elif action == "on":
            light.set_power(True)
        elif action == "second_on":
            light.set_second_power(True)
        elif action == "off":
            light.set_power(False)
        elif action == "second_off":
            light.set_second_power(False)
        elif action == "rgb":
            data = request.json
            light.set_rgb_and_brightness(data['r'], data['g'], data['b'], data['br'])
        elif action == "second_rgb":
            data = request.json
            light.set_second_rgb_and_brightness(data['r'], data['g'], data['b'], data['br'])
        elif action == "ct":
            data = request.json
            light.set_ct_and_brightness(data['ct'], data['br'])
        else:
            return Response(status=400, mimetype='application/json')
    except Exception as error:
        return Response(f'{{"error": "{repr(error)}", "traceback": "{format_exc()}"}}', status=500,
                        mimetype='application/json')
    return Response(json.dumps(light.get_info()), status=200, mimetype='application/json')


@app.route('/api/v2/scene/<scene>', methods=['POST'])
def set_scene(scene):
    try:
        return Response(json.dumps(LightRepository().set_scene(scene)), status=200, mimetype='application/json')
    except Exception as error:
        return Response(f'{{"error": "{repr(error)}", "traceback": "{format_exc()}"}}', status=500,
                        mimetype='application/json')


@app.route('/api/v2/lights', methods=['GET', 'POST', 'DELETE'])
def bulk_actions_lights():
    if request.method == 'GET':
        return Response(json.dumps(LightRepository().get_info()), status=200, mimetype='application/json')
    elif request.method == 'POST':
        return Response(json.dumps(LightRepository().set_power(True)), status=200, mimetype='application/json')
    elif request.method == 'DELETE':
        return Response(json.dumps(LightRepository().set_power(False)), status=200, mimetype='application/json')


@app.route('/api/v2/lights/<light_name>', methods=['GET'])
def light_info(light_name):
    light = LightRepository().get_light_by_name(light_name)
    if light:
        return Response(json.dumps(light.get_info()), status=200, mimetype='application/json')
    else:
        return Response(status=404, mimetype='application/json')


@app.route('/api/v2/projector', methods=['GET', 'POST'])
def projector_power():
    return Response(status=404, mimetype='application/json')


if __name__ == '__main__':
    app.run()
