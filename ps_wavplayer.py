# Wav Player with Pitch/Tempo Shift
import pyaudio
import wave
import struct
import numpy as np


def setTempo(tdata, channels, speed, channel=0):
	if channel == 0:    
		indices = np.round(np.arange(0, len(tdata), speed))
		indices = indices[indices < len(tdata)].astype(int)
		tdata = tdata[indices.astype(int)]
		return tdata
	else:
		
		indices = np.round(np.arange(0, len(tdata)/channels, speed))
		indices = indices[indices < len(tdata)/channels].astype(int)
		tdata[channel::channels] = tdata[indices.astype(int)]
	fi


CHUNKS = 1024

wf = wave.open('./audio.wav', 'rb')		# Opening audio file as binary data
p = pyaudio.PyAudio()				# Instantiate PyAudio

wav_rate = wf.getframerate()
wav_channels = wf.getnchannels()
wav_width = wf.getsampwidth()

stream = p.open(
	format = p.get_format_from_width(wav_width),
	channels = wav_channels,
	rate = wav_rate,
	output=True)

frame = wf.readframes(CHUNKS)			# Read audio raw data

while frame != '':
    tdata = struct.unpack("%dh"%(len(frame)/wav_width), frame)
    tdata = np.array(tdata)

    indices = np.round(np.arange(0, len(tdata), 1.5))
    indices = indices[indices < len(tdata)].astype(int)
    tdata = tdata[indices.astype(int)]

    frame = struct.pack("%dh"%len(tdata), *list(tdata))    

    stream.write(frame)						# Play audio
    frame = wf.readframes(CHUNKS)

stream.stop_stream()
stream.close()
p.terminate()
