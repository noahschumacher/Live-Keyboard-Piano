#!/usr/bin/env python3

## Octaves set by numbers 1-6, keyboard on a,w,s,e,d,f,t,g,y,h,u,j,and k keys

import numpy as np
import keyboard
import pyaudio
import subprocess

## Initializing PyAudio and setting parameters
PyAudio = pyaudio.PyAudio
bitrate = 16000
length = .5
frame_num = 2*int(bitrate*length)

## Initializing the audio stream
p = PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=bitrate, output=True)


## Setting the octave value
octaves = {'1':1, '2':2, '3':3, '4':4, '5':5, '6':6}
octave = 3 		# octave var init to 3, will be multiplier on frequency of sin wave


## Initing notes parameters in dictionary [Pressed, Frequency, Keyboard Key]
keys =  {'c':[False, 32.703,'a'],'csharp':[False, 34.648,'w']
		,'d':[False, 36.708,'s'],'dsharp':[False, 38.892,'e']
		,'e':[False, 41.203,'d']
		,'f':[False, 43.645,'f'],'fsharp':[False, 46.249,'t']
		,'g':[False, 48.999,'g'],'gsharp':[False, 51.913,'y']
		,'a':[False, 55.000,'h'],'asharp':[False, 58.270,'u']
		,'b':[False, 61.735,'j']
		,'c2':[False, 65.406,'k']}


## Music Data is numpy array for fast operations
for key in keys:		
	temp = np.arange(frame_num)		## Temp array allows for multiple notes to be added
	wave_data = np.sin((temp/bitrate)*2*np.pi*int(round(keys[key][1]))*(2**octave))
	keys[key].append(wave_data)
	print("The", keys[key][2], "key corresponds to a", key, "note")

## Call plotting program
subprocess.Popen("/Users/nschumacher/docs/phys129L/schumacher_homework/schumacher_project/final_project_graphing.py")
subprocess.call(["stty", "-echo"])

print("Press numbers 1 through 6 to change the octave")
print("Press escape to quit the program")
print("WARNING: DO NOT CTRL+C THIS PROGRAM, OR YOU WILL NEED TO RUN 'stty echo' TO GET YOUR INPUT BACK")
print("Please wait for graph to appear before playing")

#####################      STARTING THE STREAM LOOP     #######################
while True:

	## total_notes used to keep wave amplitude constant (volume constant)
	total_notes = 0
	output = np.zeros(frame_num)

	## Checking if Key is pressed and superimposing waves to create data for output
	for key in keys:
		if keyboard.is_pressed(keys[key][2]):
			output += keys[key][3]
			total_notes += 1

	if total_notes != 0:
		output = output/total_notes
	output = output.astype(np.float32)

	stream.write(output)


	## Reseting the octave and then the data if pressed.
	for oct in octaves:
		if keyboard.is_pressed(oct):
			octave = octaves[oct]
			for key in keys:							## Music Data numpy array
				temp = np.arange(frame_num)				## Temp array allows for multiple notes to be added
				wave_data = np.sin((temp/bitrate)*2*np.pi*int(round(keys[key][1]))*(2**octave))
				keys[key][3] = wave_data


	## Exit program when escape is pressed
	if keyboard.is_pressed('esc'):
		subprocess.call(["stty", "echo"])
		break

###############################################################################


## STOPPING THE STREAM BINDING AND TERMINATING THE CONNECTION
stream.stop_stream()
stream.close()
p.terminate
