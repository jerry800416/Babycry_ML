from scipy.io import wavfile
from scipy import signal
import numpy as np


sr, x = wavfile.read('test.wav')      # 16-bit mono 44.1 khz

b = signal.firwin(1001, cutoff=8000, fs=sr, pass_zero=False)

x = signal.filtfilt(b, [1.0], x)

wavfile.write('test2.wav', sr, x.astype(np.int16))