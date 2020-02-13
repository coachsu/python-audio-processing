# Wav Player
import pyaudio
import wave

CHUNKS = 1024						# Samples per frame

wf = wave.open('./audio.wav', 'rb')			# Opening audio file as binary data
p = pyaudio.PyAudio()					# Instantiate PyAudio

wav_channels = wf.getnchannels()
wav_rate = int(wf.getframerate())
wav_width = wf.getsampwidth()

stream = p.open(
	format = p.get_format_from_width(wav_width),
	channels = wav_channels,
	rate = wav_rate, 
	output = True)					# Open PyAudio stream for output

frame = wf.readframes(CHUNKS)				# Read wav raw data

while frame != '':
    stream.write(frame)					# Play audio
    frame = wf.readframes(CHUNKS)

stream.stop_stream()
stream.close()
p.terminate()
