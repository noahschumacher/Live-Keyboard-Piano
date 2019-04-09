#!/usr/bin/env python3

## Octaves set by numbers 1-6, keyboard on a,w,s,e,d,f,t,g,y,h,u,j,and k keys

import numpy as np
import keyboard
import matplotlib.pyplot as plt

#Remove hotkeys for matplotlib so it doesn't interfere with keyboard playing
plt.rcParams['keymap.save'] = ''
plt.rcParams['keymap.fullscreen'] = ''
plt.rcParams['keymap.grid'] = ''
plt.rcParams['keymap.all_axes'] = ''
plt.rcParams['keymap.xscale'] = ''

## Setting parameters identical to audio program
bitrate = 16000
length = .5
frame_num = 2*int(bitrate*length)

octave = 3 		# octave var init to 3, will be multiplier on frequency of sin wave

## Setting the octave value
octaves = {'1':1, '2':2, '3':3, '4':4, '5':5, '6':6}


## Initing notes parameters in dictionary [Pressed, Frequency, Keyboard Key]
keys =  {'c':[False, 32.703,'a'],'csharp':[False, 34.648,'w']
		,'d':[False, 36.708,'s'],'dsharp':[False, 38.892,'e']
		,'e':[False, 41.203,'d']
		,'f':[False, 43.645,'f'],'fsharp':[False, 46.249,'t']
		,'g':[False, 48.999,'g'],'gsharp':[False, 51.913,'y']
		,'a':[False, 55.000,'h'],'asharp':[False, 58.270,'u']
		,'b':[False, 61.735,'j']
		,'c2':[False, 65.406,'k']}


for key in keys:		## Music Data numpy array
	temp = np.arange(frame_num)			## Temp array allows for multiple notes to be added
	wave_data = np.sin((temp/bitrate)*2*np.pi*int(round(keys[key][1]))*(2**octave))
	keys[key].append(wave_data)

## Initializing Plotting with zeros for data, to be filled in later
fig, (ax, ax2) = plt.subplots(2)
fig.canvas.draw()

fft_x = np.arange(0, frame_num, 1)
fft_line, = ax2.plot(fft_x, np.zeros(frame_num))
ax2.set_xlim(3, 2000)
ax2.set_ylim(0, 1.1)
ax2.set_title("Power Spectrum")
ax2.set_xlabel("Frequency (Hz)")

x = np.arange(0, 1000, 1)
line, = ax.plot(x, np.zeros(1000))
ax.set_ylim(-1.1,1.1)
ax.set_xlim(0,1000)
ax.set_title("Waveform")
ax.set_xlabel("Frame number")

fig.show()

#####################      STARTING THE STREAM LOOP     #######################
while True:

	## total_notes used to keep wave amplitude constant (volume constant)
	total_notes = 0
	output = np.zeros(frame_num)

	## Checking if Key is pressed and recreating data that will be output as audio
	for key in keys:
		if keyboard.is_pressed(keys[key][2]):
			output += keys[key][3]
			total_notes += 1

	if total_notes != 0:
		output = output/total_notes
	output = output.astype(np.float32)


	## Reseting the octave and then the data if pressed.
	for oct in octaves:
		if keyboard.is_pressed(oct):
			octave = octaves[oct]
			for key in keys:							## Music Data numpy array
				temp = np.arange(frame_num)				## Temp array allows for multiple notes to be added
				wave_data = np.sin((temp/bitrate)*2*np.pi*int(round(keys[key][1]))*(2**octave))
				keys[key][3] = wave_data


	## Graphing the data, with ax as raw wave data and ax2 as power spectrum data, again exits if escape is pressed
	if keyboard.is_pressed('esc'):
		break
	else:
		line.set_ydata(output[0:1000])
		ax.draw_artist(ax.patch)
		ax.draw_artist(line)

		fft_data = np.fft.fft(output)
		fft_line.set_ydata(np.abs(2*fft_data[0:bitrate]/bitrate))
		ax2.draw_artist(ax2.patch)
		ax2.draw_artist(fft_line)

		fig.canvas.blit(ax2.bbox) #blitting like this makes the graphing more efficient
		fig.canvas.blit(ax.bbox)
		fig.canvas.draw()
		fig.canvas.flush_events()

