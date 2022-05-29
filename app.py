import crepe
import os
import glob
from flask import Flask, request, send_file
from flask_cors import CORS
import base64
import random
import string


app = Flask(__name__)
CORS(app)


def delete_files(start):
    files = glob.glob(start)
    for file in files:
        if file is None:
            continue
        try:
            os.remove(file)
        except:
            print("Error while deleting file : ", file)


delete_files('tmp_*')


@app.route('/')
def index():
    return ''


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str;


@app.route('/', methods=['POST'])
# request.data = wave file as byte array
def upload_file():

    hash = 'tmp_' + get_random_string(8) + '-'
    f = open(hash + 'audio', 'wb')
    f.write(request.data)

    with open(hash + 'audio', 'r') as input_file:
      coded_string = input_file.read()
    decoded = base64.b64decode(coded_string)
    with open(hash + 'audio_decoded', 'wb') as output_file:
      output_file.write(decoded)
    try:
        os.remove(hash + 'audio.wav')
    except:
        None
    os.system('ffmpeg -i ' + hash + 'audio_decoded ' + hash + 'audio.wav')
    os.system('./noiseclean.sh ' + hash + 'audio.wav ' + hash + 'result.wav')

    crepe.process_file(
        file=hash + 'result.wav',
        # output='',  # output directory
        model_capacity='medium',  # medium, full
        viterbi=True,  # ?
        center=True,  # ?
        save_activation=False,  # matrice des données
        save_plot=True,
        plot_voicing=False,
        step_size=10,
        verbose=True
    )
    image = hash + 'result.activation.png'
    return send_file(image, attachment_filename=image)
