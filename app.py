from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from collections import OrderedDict
import json
from PIL import Image
import numpy as np
from tensorflow import keras
import tensorflow_hub as hub
app = Flask(__name__)
max_size = 10 * 1024 * 1024  
breed_list = ['affenpinscher', 'afghan_hound', 'african_hunting_dog', 'airedale',
       'american_staffordshire_terrier', 'appenzeller',
       'australian_terrier', 'basenji', 'basset', 'beagle',
       'bedlington_terrier', 'bernese_mountain_dog',
       'black-and-tan_coonhound', 'blenheim_spaniel', 'bloodhound',
       'bluetick', 'border_collie', 'border_terrier', 'borzoi',
       'boston_bull', 'bouvier_des_flandres', 'boxer',
       'brabancon_griffon', 'briard', 'brittany_spaniel', 'bull_mastiff',
       'cairn', 'cardigan', 'chesapeake_bay_retriever', 'chihuahua',
       'chow', 'clumber', 'cocker_spaniel', 'collie',
       'curly-coated_retriever', 'dandie_dinmont', 'dhole', 'dingo',
       'doberman', 'english_foxhound', 'english_setter',
       'english_springer', 'entlebucher', 'eskimo_dog',
       'flat-coated_retriever', 'french_bulldog', 'german_shepherd',
       'german_short-haired_pointer', 'giant_schnauzer',
       'golden_retriever', 'gordon_setter', 'great_dane',
       'great_pyrenees', 'greater_swiss_mountain_dog', 'groenendael',
       'ibizan_hound', 'irish_setter', 'irish_terrier',
       'irish_water_spaniel', 'irish_wolfhound', 'italian_greyhound',
       'japanese_spaniel', 'keeshond', 'kelpie', 'kerry_blue_terrier',
       'komondor', 'kuvasz', 'labrador_retriever', 'lakeland_terrier',
       'leonberg', 'lhasa', 'malamute', 'malinois', 'maltese_dog',
       'mexican_hairless', 'miniature_pinscher', 'miniature_poodle',
       'miniature_schnauzer', 'newfoundland', 'norfolk_terrier',
       'norwegian_elkhound', 'norwich_terrier', 'old_english_sheepdog',
       'otterhound', 'papillon', 'pekinese', 'pembroke', 'pomeranian',
       'pug', 'redbone', 'rhodesian_ridgeback', 'rottweiler',
       'saint_bernard', 'saluki', 'samoyed', 'schipperke',
       'scotch_terrier', 'scottish_deerhound', 'sealyham_terrier',
       'shetland_sheepdog', 'shih-tzu', 'siberian_husky', 'silky_terrier',
       'soft-coated_wheaten_terrier', 'staffordshire_bullterrier',
       'standard_poodle', 'standard_schnauzer', 'sussex_spaniel',
       'tibetan_mastiff', 'tibetan_terrier', 'toy_poodle', 'toy_terrier',
       'vizsla', 'walker_hound', 'weimaraner', 'welsh_springer_spaniel',
       'west_highland_white_terrier', 'whippet',
       'wire-haired_fox_terrier', 'yorkshire_terrier']
model = None

def getModel():
    load_model = keras.models.load_model('Dogs_Breed_Prediction_WebApp-master\static\model\\full-image-set-mobilenetv2-adam.h5',custom_objects={'KerasLayer': hub.KerasLayer})
    print('Keras Model Loading finished.')
    return load_model

model = getModel()

def preprocessImage(image,target_size):
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize(target_size)
    image = keras.preprocessing.image.img_to_array(image)
    image = keras.applications.mobilenet.preprocess_input(image)
    image = np.expand_dims(image,0)
    return image


@app.route('/')
def index():
    return render_template('Prediction/index.html')


@app.route('/about')
def about():
    return render_template('Prediction/about.html',breed_list = breed_list,length=int(len(breed_list)/3))


supported_type = ['image/png', 'image/jpeg']


@app.route('/prediction', methods=['POST'])
def prediction():
    if 'file' not in request.files:
        # No file
        return {"Error": "No File Object Found."}, 400

    if request.content_length > (max_size+1000):
        return {"Error": f"File size must be less than {max_size/(1024*1024)} MB"},400

    file = request.files['file']

    # if user does not select file, browser also submit an empty part without filename
    if file.filename == '':
        return {"Error": "File not selected. Empty File!"}, 400

    mime_type = file.content_type
    if file and mime_type in supported_type:
        # filename = secure_filename(file.filename)
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) # to save the Image
        image = Image.open(file)
        processed_image = preprocessImage(image,target_size=(224,224))
        global model
        if model == None:
        	model = getModel()
        predicted_data = model.predict(processed_image)
        # class_index = np.argmax(predicted_data)
        sorted_index = predicted_data.argsort()
        top_5_prediction = OrderedDict()
        for i in range(1,6):
            top_5_prediction[breed_list[sorted_index[0,-i]]] = str(predicted_data[0,sorted_index[0,-i]])

        # success return
        return json.dumps(top_5_prediction), 200
    else:
        return {"Error": "File type not supported."}, 400



@app.errorhandler(404)
def exception(ex):
    return render_template('404.html')

if __name__ == '__main__':
    print('Loading Keras Model.')
    app.run(debug=False,host='0.0.0.0')
