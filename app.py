import json

from flask import Flask, request, Response
from ir_denon import IrDenon
from light_helper import LightHelper
from smart_tv import SmartTv
from spotify_helper import SpotifyHelper, SpotiLightException


app = Flask(__name__)

@app.route('/api/v1/bulb/<int:bulb_id>', methods=['GET'])
def get_bulb(bulb_id):
    try:
        bulb_data = LightHelper().bulb_info(bulb_id)
        return Response(json.dumps(bulb_data), status=200, mimetype='application/json')
    except AttributeError as error:
        return Response(f'{{"error_message": "{error}"}}', status=500, mimetype='application/json')

@app.route('/api/v1/bulb/<int:bulb_id>/<int:light_type>/<action>', methods=['POST'])
def action_bulb(bulb_id, light_type, action):
    try:
        LightHelper().bulb(bulb_id, light_type, action, **(request.json or {}))
        return Response(status=200, mimetype='application/json')
    except AttributeError as error:
        return Response(f'{{"error_message": "{error}"}}', status=500, mimetype='application/json')

@app.route('/api/v1/spotify', methods=['GET'])
def get_spotify():
    try:
        return Response(f'{{"best_rgb": {str(SpotifyHelper().get_color_from_currently_played_album())}}}',
                        status=200,
                        mimetype='application/json')
    except (SpotiLightException, AttributeError) as error:
        return Response(f'{{"error_message": "{error}"}}',
                        status=500,
                        mimetype='application/json')

@app.route('/api/v1/denon', methods=['GET'])
def get_denon():
    return Response(IrDenon().to_json(), status=200, mimetype='application/json')

@app.route('/api/v1/denon/<action>', methods=['POST'])
def action_denon(action):
    try:
        IrDenon().send(action, request.json['count'])
        return Response(IrDenon().to_json(), status=200, mimetype='application/json')
    except Exception as error:
        return Response(f'{{"error_message": "{error}"}}', status=500, mimetype='application/json')

@app.route('/api/v1/tv', methods=['DELETE'])
def set_all_smart_tv_apps_off():
    return SmartTv().set_all_apps_off()

@app.route('/api/v1/tv/<app_name>', methods=['GET', 'POST', 'DELETE'])
def smart_tv_app(app_name):
    if request.method == 'GET':
        return SmartTv().get_app_status(app_name)
    elif request.method == 'POST':
        return SmartTv().set_app_on(app_name)
    elif request.method == 'DELETE':
        return SmartTv().set_app_off(app_name)

if __name__ == '__main__':
    app.run()
