# Wav Player
import sys
import pyaudio
import wave
import struct
import numpy as np
import volctrl as vc
import tempoctrl as tc
import threading
import os

FILE = sys.argv[1]
VOL = float(sys.argv[2])
TEMPO = float(sys.argv[3])
CHUNKS = 1024						# Samples per frame

def control():
	global VOL
	global TEMPO
	while True:
		os.system('clear')
		print 'VOL = ' + str(VOL) + '; TEMPO = ' + str(TEMPO)
		cmd = raw_input("CMD[u for VOL up, d for VOL down, f for speed up, and s for slow down]: ")
		if cmd == "u":
			VOL = VOL + 0.1
			if VOL > 1:
				VOL = 1.0
		elif cmd == "d":
			VOL = VOL - 0.1
			if VOL < 0.1:
				VOL = 0.1
		elif cmd == "f":
			TEMPO = TEMPO + 0.1
			if TEMPO > 2:
				TEMPO = 2.0
		elif cmd == "s":
			TEMPO = TEMPO - 0.1
			if TEMPO < 0.5:
				TEMPO = 0.5

t = threading.Thread(target = control)
t.start()

wf = wave.open(FILE, 'rb')				# Opening audio file as binary data
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
	tdata = struct.unpack("%dh"%(len(frame)/wav_width), frame)
	tdata = np.array(tdata)

	tdata = vc.setvol(tdata, VOL)
	tdata = tc.settempo(tdata, TEMPO)

	frame = struct.pack("%dh"%(len(tdata)), *list(tdata))

	stream.write(frame)					# Play audio
	frame = wf.readframes(CHUNKS)

t.join()

stream.stop_stream()
stream.close( )
p.terminate()
