from flask import request, Flask, jsonify
import os

app = Flask(__name__)

models = {}
model_path = os.path.abspath('./models/YOLO8segN-795.pt')

cameras = []
for idx, filename in enumerate(os.listdir('./cameras')):
    if filename.lower().endswith(('.mp4', '.mov', '.avi')):
        cameras.append({'ip': os.path.abspath(f'./cameras/{filename}'), 'id': idx, 'description': filename},)

for camera in cameras:
    models[camera['id']] = model_path

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
        return 'No selected fil', 400

    image_file.save(r'C:\Users\boiko.k.v\Desktop\Carbon-Digital-Twin\diagnostic_modul\images-save' + image_file.filename)

    return 'Image archived for camera {}'.format(camera_id), 200
    

    
if __name__ == '__main__':
    app.run(debug=True)