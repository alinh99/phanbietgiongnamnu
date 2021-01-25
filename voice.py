import sounddevice as sd
from scipy.io.wavfile import write
import os
from scipy.io.wavfile import read
from csv import DictWriter
import pandas as pd

fs = 44100
seconds = 5

my_recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
print("Starting: Speak now!")
sd.wait()
print("finished")
write('output.wav', fs, my_recording)
os.startfile("output.wav")

data = pd.read_csv("input/voice.csv")

data.label = [1 if each == 'male' else 0 for each in data.label]
# print(data)

male = data[data.label == 1]
female = data[data.label == 0]


def append_dict_as_row(file_name, dict_of_elem, field_names):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        dict_writer = DictWriter(write_obj, fieldnames=field_names)
        # Add dictionary as wor in the csv
        dict_writer.writerow(dict_of_elem)


field_names = ['meanfreq', 'sd', 'median', 'Q25', 'Q75', 'IQR', 'skew', 'kurt', 'sp.ent', 'sfm', 'mode', 'centroid',
               'meanfun', 'minfun', 'maxfun', 'meandom', 'mindom', 'maxdom', 'dfrange', 'modindx', 'label']
data = read('output.wav')
row_dict = {'meanfreq': data}
append_dict_as_row('input/voice_test.csv', row_dict, field_names)
# gender_voice = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_ALL)
