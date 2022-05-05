import crepe
import os
import base64

#os.system('ffmpeg -i audio audio.wav')

crepe.process_file(
        file='audio.wav',
        # output='',  # output directory
        model_capacity='full',  # medium, full
        viterbi=True,  # ?
        center=True,  # ?
        save_activation=False,  # matrice des donnees
        save_plot=True,
        plot_voicing=False,
        step_size=5,
        verbose=True
        )
