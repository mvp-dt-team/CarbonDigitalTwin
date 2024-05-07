from flask import request, Flask, jsonify
import os
import datetime
import pandas as pd


app = Flask(__name__)

models = {}
model_path = os.path.abspath('./models/YOLO8segN-795.pt')

cameras = []
for idx, filename in enumerate(os.listdir('./cameras')):
    if filename.lower().endswith(('.mp4', '.mov', '.avi')):
        cameras.append({'ip': os.path.abspath(f'./cameras/{filename}'), 'id': idx, 'description': filename},)

for camera in cameras:
    models[camera['id']] = model_path

### Модуль компьютерного зрения

@app.route('/camera')
def camera():
    return jsonify(cameras)
    
@app.route('/camera/<camera_id>/model', methods=['GET', 'POST'])
def get_model(camera_id):
    camera_id = int(camera_id)
    if camera_id in [key for key, _ in models.items()]:
        text = None
        with open(models[camera_id], 'rb') as model:
            text = model.read()
        return text
    else:
        return 1
    
@app.route('/camera/<camera_id>', methods=['GET', 'POST'])
def set_value(camera_id):
    if request.headers['Content-Type'] == 'application/json':
        data = request.json
        
        value = data['value']
        print(f'Получены данные с камеры: {value}')
        return jsonify({'message': f'Data received for camera {camera_id}. Value: {value}'}), 200
    else:
        return jsonify({'error': 'Unsupported Media Type'}), 415
    
@app.route('/camera/<camera_id>/archivate', methods=['GET', 'POST'])
def archivate(camera_id):
    if 'image' not in request.files:
        return 'No image file in request', 400

    image_file = request.files['image']
    if image_file.filename == '':
        return 'No selected file', 400

    image_file.save(r'C:\Users\boiko.k.v\Desktop\Carbon-Digital-Twin\diagnostic_modul\images-save' + image_file.filename)

    return 'Image archived for camera {}'.format(camera_id), 200
    
### Модуль предсказания свойств

measurement_sources = [
  {
    "id": 0,
    "name": "universal 1",      
    "unit": 1
  },
  {
    "id": 1,
    "name": "universal 2",
    "unit": 2
  }
]
units = [[
    {
    "description": "Pressure_unit1",
    "installation_time": "2020-01-01T00:00:00Z",
    "deactivation_time": "2021-01-01T00:00:00Z",
    "model_name": "Модель A"
  },
  {
    "description": "Temperature_unit1",
    "installation_time": "2020-05-01T00:00:00Z",
    "deactivation_time": None,
    "model_name": "Модель A"
  },
  {
    "description": "Humidity_unit1",
    "installation_time": "2020-05-01T00:00:00Z",
    "deactivation_time": None,
    "model_name": "Модель A"
  }
],
[
  {
    "description": "Temperature_unit2",
    "installation_time": "2020-05-01T00:00:00Z",
    "deactivation_time": None,
    "model_name": "Модель B"
  },
  {
    "description": "Pressure_unit2",
    "installation_time": "2020-05-01T00:00:00Z",
    "deactivation_time": None,
    "model_name": "Модель B"
  }
]]

@app.route('/measurement_source')
def measurement_source():
    return jsonify(measurement_sources)

@app.route('/sensors_by_source')
def get_sensor_data():
    sensor_id = request.args.get('id')
    return jsonify(units[int(sensor_id)])

@app.route('/measurement_data', methods=['POST'])
def process_measurement_data():
    data = request.json

    if data is None or 'measurements' not in data:
        return jsonify({"error": "Invalid request format"}), 400

    measurements = data['measurements']
    response_data = []

    for measurement in measurements:
        sensor_id = int(measurement.get('sensor_id'))
        measurement_source_id = int(measurement.get('measurement_source_id'))
        time_from = datetime.datetime.strptime(measurement.get('time_from'), "%Y-%m-%dT%H:%M:%SZ")
        time_to = datetime.datetime.strptime(measurement.get('time_to'), "%Y-%m-%dT%H:%M:%SZ")

        data_for_measurement = get_data_source(sensor_id, measurement_source_id, time_from, time_to)
        response_data.append(data_for_measurement)

    return jsonify(response_data)

def get_data_source(sensor_id, measurement_source_id,  time_from, time_to):
    df = pd.read_csv('data.csv')
    df['Time'] = pd.to_datetime(df['Time'])
    filtered_df = df[(df['Time'] >= time_from) & (df['Time'] <= time_to)]

    sensor_name = units[measurement_source_id][sensor_id]['description']

    return {
        "measurement_source_id": sensor_id,
        "data": filtered_df[sensor_name].tolist()
    }

"""
Передаваемое значение JSON
{
"sources": [0, 1, 2, 3, 4, 5],
"property_names": ["elastic_modulus"],
"values": [19.231]
}

"""
@app.route('/save_prediction_data', methods=['POST'])
def save_data_prediction():
    data = request.json
    sources = data['sources']
    property_names = data['property_names']
    values = data['values']

    print(f'Получены следуещие данные: источники({sources}), названия свойств({property_names}), значения({values})')

    return {'status': 'ok'}

if __name__ == '__main__':
    app.run(debug=True)