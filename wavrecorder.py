# Wave Recorder
import pyaudio
import wave

CHUNKS = 1024					# Samples per frame
FORMAT = pyaudio.paInt16			# Sample depth: 16 bits
CHANNELS = 2					# Channels (1 for mono, 2 for stereo)
RATE = 44100					# Samples per second
DURATION = 5					# Recording time (seconds)

p = pyaudio.PyAudio()				# Instantiate PyAudio

stream = p.open(
	format = FORMAT,
	channels = CHANNELS,
	rate = RATE, 
	input = True)				# PyAudio stream for input

frame = []

for i in range(0, int(RATE / CHUNKS * DURATION)):
    data = stream.read(CHUNKS)	
    frame.append(data)

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open('./audio.wav', 'wb')		# Opening audio file as binary data
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frame))
wf.close()
