# Wav Player with Pitch/Tempo Shift
import pyaudio
import wave
import struct
import numpy as np
import sys

# tdata: audio samples in time domain represented by Numpy array
# channels: the number of channels
# speed: > 1 for speec up, < 1 for slow down
# channel: 0 for all channels, n > 0 for one channel
def settempo(tdata, speed):
	indices = np.round(np.arange(0, len(tdata), speed))
	indices = indices[indices < len(tdata)].astype(int)
	tdata = tdata[indices.astype(int)]
	return tdata

if __name__ == '__main__':
	FILE = sys.argv[1]
	TEMPO = float(sys.argv[2])
	CHUNKS = 1024

	wf = wave.open(FILE, 'rb')		# Opening audio file as binary data
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

		tdata = settempo(tdata, TEMPO)

		frame = struct.pack("%dh"%len(tdata), *list(tdata))    
		stream.write(frame)						# Play audio
		frame = wf.readframes(CHUNKS)

	stream.stop_stream()
	stream.close()
	p.terminate()
