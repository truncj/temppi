import json
import logging

from flask import Flask, jsonify
from w1thermsensor import W1ThermSensor, NoSensorFoundError

app = Flask(__name__)


@app.route('/', methods=['GET'])
def about():
    return jsonify({'Status': 'UP'})


@app.route('/temp', methods=['GET'])
def temp():
    temperature = 0

    with open('config/config.json') as f:
        data = json.load(f)
        room = data['room']

    try:
        sensors = W1ThermSensor().get_available_sensors()
    except NoSensorFoundError:
        # attempt to solve "Task exception was never retrieved" and "w1thermsensor.errors.NoSensorFoundError"
        logging.error('NoSensorFoundError')
        return

    for sensor in sensors:
        try:
            temperature = sensor.get_temperature()
        except IndexError as error:
            logging.error(f'temperature sensor is unavailable - {error}')
            return

    tf = round(9.0 / 5.0 * temperature + 32, 2)

    return jsonify({
        'temp': tf,
        'room': room
    })


app.run(host='0.0.0.0', port=3000, debug=True)
