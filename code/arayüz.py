import pygame
import sounddevice as sd
import numpy as np
import pyaudio

pygame.init()

win = pygame.display.set_mode((800, 600))
image = pygame.image.load('gitar.jpg')
win.fill((255,255,255))

class button(): 
	def __init__(self, color, x, y, width, height, text=''): 
		self.color = color 
		self.x = x 
		self.y = y 
		self.width = width 
		self.height = height 
		self.text = text

	def draw(self,win,outline=None):
		if outline:
			pygame.draw.rect(win, outline, (self.x - 5, self.y - 5, self.width + 10, self.height + 10), 0)

		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0) 
		if self.text != '': 
			font = pygame.font.SysFont('modern', 60) 
			text = font.render(self.text, 1, (0,0,0)) 
			win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

	def isOver(self, pos):
		if pos[0] > self.x and pos[0] < self.x + self.width: 
			if pos[1] > self.y and pos[1] < self.y + self.height: 
				return True
		return False

class note_window():
	def __init__(self, color, x, y, width, height, text=''):
		self.color = color
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.text = text
	def draw(self, win):
		if self.text != '':
			pygame.draw.rect(win, self.color, (self.x - 43, self.y - 10, self.width + 90, self.height + 4), 0)
			font = pygame.font.SysFont('modern', 60)
			text = font.render(self.text, 1, (0,0,0))
			win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

def readWindow():
	win.fill((255,255,255))
	win.blit(image, [0,0])
	kalınmi_Button.draw(win, (255,165,0))
	la_Button.draw(win, (255,165,0))
	re_Button.draw(win, (255,165,0))
	sol_Button.draw(win, (255,165,0))
	si_Button.draw(win, (255,165,0))
	incemi_Button.draw(win, (255,165,0))
	
kalınmi_Button = button((255,0,0), 60, 330, 150, 50, 'kalın mi')
la_Button = button((255,0,0), 60, 212, 150, 50, 'la')
re_Button = button((255,0,0), 60, 100, 150, 50, 're')
sol_Button = button((255,0,0), 590, 100, 150, 50, 'sol')
si_Button = button((255,0,0), 590, 212, 150, 50, 'si')
incemi_Button = button((255,0,0), 590, 330, 150, 50, 'ince mi')

NOTE_MIN = 40      
NOTE_MAX = 64      
FSAMP = 44100       
FRAME_SIZE = 2048  
FRAMES_PER_FFT = 16 

SAMPLES_PER_FFT = FRAME_SIZE * FRAMES_PER_FFT
FREQ_STEP = float(FSAMP) / SAMPLES_PER_FFT

NOTE_NAMES = 'mi fa fadiyez sol soldiyez la ladiyez si do dodiyez re rediyez'.split()

def freq_to_number(f): 
    return 64 + 12 * np.log2(f / 329.63)

def number_to_freq(n): 
    return 329.63 * 2**((n - 64) / 12.0)

def note_name(n):
    return NOTE_NAMES[n % NOTE_MIN % len(NOTE_NAMES)] + str(int(n / 12 - 1))

def note_to_fftbin(n): 
    return number_to_freq(n) / FREQ_STEP

imin = max(0, int(np.floor(note_to_fftbin(NOTE_MIN - 1))))
imax = min(SAMPLES_PER_FFT, int(np.ceil(note_to_fftbin(NOTE_MAX + 1))))

buf = np.zeros(SAMPLES_PER_FFT, dtype=np.float32)
num_frames = 0

stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=FSAMP, input=True, frames_per_buffer=FRAME_SIZE)
stream.start_stream()

window = 0.5 * (1 - np.cos(np.linspace(0, 2 * np.pi, SAMPLES_PER_FFT, False)))

while stream.is_active():
	buf[:-FRAME_SIZE] = buf[FRAME_SIZE:]
	buf[-FRAME_SIZE:] = np.fromstring(stream.read(FRAME_SIZE), np.int16)
	fft = np.fft.rfft(buf * window)
	freq = (np.abs(fft[imin:imax]).argmax() + imin) * FREQ_STEP
	n = freq_to_number(freq)
	n0 = int(round(n))
	num_frames += 1
	if num_frames >= FRAMES_PER_FFT:
		print('sayı: {:7.2f}     frekans: {:7.2f} Hz     nota: {:>3s} {:+.2f}'.format(n, freq, note_name(n0), n - n0))
	readWindow()
	pygame.display.update()
	note = note_window((0,255,0), 350, 50, 100, 50, note_name(n0))
	note.draw(win)
	pygame.display.update()
	for event in pygame.event.get():
		pos = pygame.mouse.get_pos()
		if event.type == pygame.QUIT:
			run = False
			pygame.quit()
			quit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			if kalınmi_Button.isOver(pos):
				sd.play(2*np.sin(2*np.pi*82.41*np.arange(44100)/44100), samplerate=44100, blocking=True)
				print("kalınmi Button")
			elif la_Button.isOver(pos):
				sd.play(2*np.sin(2*np.pi*110.00*np.arange(44100)/44100), samplerate=44100, blocking=True)
				print("la Button")
			elif re_Button.isOver(pos):
				sd.play(2*np.sin(2*np.pi*146.83*np.arange(44100)/44100), samplerate=44100, blocking=True)
				print("re Button")
			elif sol_Button.isOver(pos):
				sd.play(2*np.sin(2*np.pi*196.00*np.arange(44100)/44100), samplerate=44100, blocking=True)
				print("sol Button")
			elif si_Button.isOver(pos):
				sd.play(2*np.sin(2*np.pi*246.94*np.arange(44100)/44100), samplerate=44100, blocking=True)
				print("si Button")
			elif incemi_Button.isOver(pos):
				sd.play(2*np.sin(2*np.pi*329.63*np.arange(44100)/44100), samplerate=44100, blocking=True)
				print("incemi Button")
		if event.type == pygame.MOUSEMOTION:
			if kalınmi_Button.isOver(pos):
				kalınmi_Button.color = (255,0,0)
			elif la_Button.isOver(pos):
				la_Button.color = (255,0,0)
			elif re_Button.isOver(pos):
				re_Button.color = (255,0,0)
			elif sol_Button.isOver(pos):
				sol_Button.color = (255,0,0)
			elif si_Button.isOver(pos):
				si_Button.color = (255,0,0)
			elif incemi_Button.isOver(pos):
				incemi_Button.color = (255,0,0)
			else:
				kalınmi_Button.color = (128,128,128)
				la_Button.color = (128,128,128)
				re_Button.color = (128,128,128)
				sol_Button.color = (128,128,128)
				si_Button.color = (128,128,128)
				incemi_Button.color = (128,128,128)