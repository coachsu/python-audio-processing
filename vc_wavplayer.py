# Wav Player with Voice Control
import pyaudio
import wave
import struct
import numpy as np


def setVol(tdata, percent, channel=0):
	if channel == 0:
		return tdata * percent						# All channels
	else:
		tdata[channel::2] = tdata[channel::2] * percent			# Only one channel
		return tdata
	fi

if __name__ == '__main__':

	CHUNKS = 1024
	wf = wave.open('./audio.wav', 'rb')					# Opening audio file as binary data
	p = pyaudio.PyAudio()							# Instantiate PyAudio

	width = wf.getsampwidth()
	stream = p.open(
		format = p.get_format_from_width(width),
		channels = wf.getnchannels(),
		rate = wf.getframerate(),
		output = True)

	frame = wf.readframes(CHUNKS)						# Read audio raw data

	while frame != '':
		# Convert binary data to Python array
		tdata = struct.unpack("%dh"%(len(frame)/width), frame)
		# Convert Python array to Numpy array
		tdata = np.array(tdata)

		# Voice control here (changing amplitude)
		tdata = setFrameVol(tdata, 0.5)

		# Convert Numpy array to binary data
		frame = struct.pack("%dh"%len(tdata), *list(tdata))    

		stream.write(frame)						# Play audio
		frame = wf.readframes(CHUNKS)

	stream.stop_stream()
	stream.close()
	p.terminate()
