import json

from ir_denon import IrDenon
from flask import Flask, request, Response
from light_helper import LightHelper, SpotiLightException


app = Flask(__name__)

@app.route('/api/v1/bulb/<int:bulb_id>', methods=['GET'])
def bulb_get(bulb_id):
    try:
        bulb_data = LightHelper().bulb_info(bulb_id)
        return Response(json.dumps(bulb_data), status=200, mimetype='application/json')
    except AttributeError as error:
        return Response(f'{{"error_message": "{error}"}}', status=500, mimetype='application/json')

@app.route('/api/v1/bulb/<int:bulb_id>/<int:light_type>/<action>', methods=['POST'])
def bulb_action(bulb_id, light_type, action):
    try:
        LightHelper().bulb(bulb_id, light_type, action, **(request.json or {}))
        return Response(status=200, mimetype='application/json')
    except AttributeError as error:
        return Response(f'{{"error_message": "{error}"}}', status=500, mimetype='application/json')

@app.route('/api/v1/spotify', methods=['GET'])
def spotify_get():
    try:
        return Response(f'{{"best_rgb": {str(LightHelper().single_spotify())}}}',
                        status=200,
                        mimetype='application/json')
    except (SpotiLightException, AttributeError) as error:
        return Response(f'{{"error_message": "{error}"}}',
                        status=500,
                        mimetype='application/json')

@app.route('/api/v1/spotify/<action>', methods=['POST'])
def spotify_action(action):
    try:
        if action == "start":
            LightHelper().start_spotify()
        elif action == "stop":
            LightHelper().stop_spotify()
        return Response(status=200, mimetype='application/json')
    except SpotiLightException as error:
        return Response(f'{{"error_message": "{error}"}}', status=500, mimetype='application/json')

@app.route('/api/v1/denon/<command>', methods=['POST'])
def denon(command):
    try:
        IrDenon().send(command, request.json['count'])
        return Response(status=200, mimetype='application/json')
    except Exception as error:
        return Response(f'{{"error_message": "{error}"}}', status=500, mimetype='application/json')


if __name__ == '__main__':
    app.run()
