# Wav Player with Voice Control
import sys
import pyaudio
import wave
import struct
import numpy as np

# tdata: audio samples in time domain represented as Numpy array
# percent: 0.1 ~ 1
# channel: 0 for all channels, > 0 for single channel
def setvol(tdata, percent=1, channel=0):
	# Volume can be set between 0.1 and 1
	if percent > 1:
		percent = 1
	if percent < 0.1:
		percent = 0.1

	if channel == 0:							# All channels
		return tdata * percent					
	else:									# One channel
		tdata[(channel-1)::2] = tdata[(channel-1)::2] * percent
		return tdata
	fi

if __name__ == '__main__':
	FILE = sys.argv[1]
	VOL = float(sys.argv[2])
	CHL = int(sys.argv[3])
	CHUNKS = 1024

	wf = wave.open(FILE, 'rb')						# Opening audio file as binary data
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
		tdata = setvol(tdata, VOL, CHL)

		# Convert Numpy array to binary data
		frame = struct.pack("%dh"%len(tdata), *list(tdata))    

		stream.write(frame)						# Play audio
		frame = wf.readframes(CHUNKS)

	stream.stop_stream()
	stream.close()
	p.terminate()
