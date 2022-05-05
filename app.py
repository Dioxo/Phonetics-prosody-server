import crepe
import os
from flask import Flask, request, send_file
from flask_cors import CORS
import base64


app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return ''


@app.route('/', methods=['POST'])
# request.data = wave file as byte array
def upload_file():

    f = open('audio', 'wb')
    f.write(request.data)

    with open('audio', 'r') as input_file:
      coded_string = input_file.read()
    decoded = base64.b64decode(coded_string)
    with open('audio_decoded', 'wb') as output_file:
      output_file.write(decoded)
    try:
        os.remove('audio.wav')
    except:
        None
    os.system('ffmpeg -i audio_decoded audio.wav')

    crepe.process_file(
        file='audio.wav',
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
    image = 'audio.activation.png'
    return send_file(image, attachment_filename=image)
