import json

from ir_denon import IrDenon
from flask import Flask, request, Response
from spoti_light import SpotiLight, SpotiLightException


app = Flask(__name__)

@app.route('/api/v1/bulb/<int:bulb_id>', methods=['GET'])
def bulb_get(bulb_id):
    try:
        bulb_data = SpotiLight().bulb_info(bulb_id)
        return Response(json.dumps(bulb_data), status=200, mimetype='application/json')
    except AttributeError as error:
        return Response(f'{{"error_message": "{error}"}}', status=500, mimetype='application/json')

@app.route('/api/v1/bulb/<int:bulb_id>/<int:light_type>/<action>', methods=['POST'])
def bulb_action(bulb_id, light_type, action):
    try:
        SpotiLight().bulb(bulb_id, light_type, action, **(request.json or {}))
        return Response(status=200, mimetype='application/json')
    except AttributeError as error:
        return Response(f'{{"error_message": "{error}"}}', status=500, mimetype='application/json')

@app.route('/api/v1/spotify/<action>', methods=['POST'])
def spotify(action):
    try:
        if action == "start":
            SpotiLight().start_spotify()     
        elif action == "stop":
            SpotiLight().stop_spotify()
        elif action == "single":
            SpotiLight().single_spotify()
        return Response(status=200, mimetype='application/json')
    except SpotiLightException as error:
        return Response(f'{{"error_message": "{error}"}}', status=500, mimetype='application/json')

@app.route('/api/v1/denon/<command>', methods=['POST'])
def denon(command):
    try:
        IrDenon.send(command, int(request.json['count']))
        return Response(status=200, mimetype='application/json')
    except Exception as error:
        return Response(f'{{"error_message": "{error}"}}', status=500, mimetype='application/json')


if __name__ == '__main__':
    app.run()
