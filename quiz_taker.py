from random import randint, choice
import pygame.midi
import os
import wx

keys = [['c'], ['cis', 'des'], ['d'], ['dis', 'ees'], ['e'], ['f'], ['fis', 'ges'], ['g'], ['gis', 'aes'], ['a'], ['ais', 'bes'], ['b']]
res_form = lambda x: keys[x % 12]
octave_designation_form = lambda x: ((x - 12) // 12)
get_pitch_name = lambda x: f"{choice(res_form(x))}{octave_designation_form(x)}"

random_notes = []

class InitialPanel(wx.Panel):
	def __init__(self, parent, switch_callback):
		super().__init__(parent)
		self.switch_callback = switch_callback

		main_sizer = wx.BoxSizer(wx.VERTICAL)

		self.combo_1_label = wx.StaticText(self, label= "", pos=(30, 30))
		self.combo_1 = wx.ComboBox(self, choices = [f"{get_pitch_name(i)}" for i in range(21, 109)], pos=(30, 50))
		self.combo_2 = wx.ComboBox(self, choices = [f"{get_pitch_name(i)}" for i in range(21, 109)], pos=(30, 50))


		main_sizer.Add(wx.StaticText(self, label="What is the lowest note you'd like to learn?"), flag=wx.ALL, border=5)
		main_sizer.Add(self.combo_1, flag=wx.ALL, border=1)
		main_sizer.Add(wx.StaticText(self, label="What is the highest note you'd like to learn?"), flag=wx.ALL, border=5)
		main_sizer.Add(self.combo_2, flag=wx.ALL, border=1)


		self.checkbox1 = wx.CheckBox(self, label="Use black keys")
		self.checkbox2 = wx.CheckBox(self, label="Use white keys")

		main_sizer.Add(self.checkbox1, flag=wx.ALL, border=5)
		main_sizer.Add(self.checkbox2, flag=wx.ALL, border=5)


		btn1 = wx.Button(self, label="Generate Notes")
		btn2 = wx.Button(self, label="Take Quiz")

		btn1.Bind(wx.EVT_BUTTON, self.btn_read_settings)
		btn2.Bind(wx.EVT_BUTTON, self.switch_screen)

		main_sizer.Add(btn1, flag=wx.ALL, border=5)
		main_sizer.Add(btn2, flag=wx.ALL, border=5)

		self.SetSizer(main_sizer)

	def switch_screen(self, event):
		self.switch_callback()
	
	def btn_read_settings(self, event):
		lower_bound = int(self.combo_1.GetCurrentSelection()) + 21
		upper_bound = int(self.combo_2.GetCurrentSelection()) + 21
		use_black_keys = self.checkbox1.GetValue()
		use_white_keys = self.checkbox2.GetValue()


		if lower_bound >= 21 and upper_bound >= 21 and (lower_bound + 1) < upper_bound and (use_black_keys or use_white_keys):
			print("VALID")
			print(lower_bound)
			print(upper_bound)
			self.__generate_notes(lower_bound, upper_bound, use_black_keys, use_white_keys)
		if lower_bound == -1:
			print("Please choose a lower bound")
		if upper_bound == -1:
			print("Please choose an upper bound")
		if upper_bound <= lower_bound:
			print("Please make sure the upper bound is higher than the lower bound")
		if not use_white_keys and not use_black_keys:
			print("Choose at least one of the type of keys to use")
	
	def __generate_notes(self, lower_bound, upper_bound, use_black_keys, use_white_keys):
		iterations = 100
		black_keys = [1, 3, 6, 8, 10]
		white_keys = [0, 2, 4, 5, 7, 9, 11]
		possible_keys = [i for i in range(12)]

		if use_black_keys and not use_white_keys:
			possible_keys = black_keys
		elif use_white_keys and not use_black_keys:
			possible_keys = white_keys
		
		print(possible_keys)
		
		sheets = self.create_new_note_file(lower_bound, upper_bound, iterations, possible_keys)
		self.write_sheets(sheets)
		self.create_random_sheets(iterations)

	def midi_to_lilypond(self, note):
		tone = choice(res_form(note))
		octave_destination = octave_designation_form(note)
		dist = octave_destination - 3
		return tone + dist * '\'' + (-dist) * ','

	def create_new_note_file(self, min_range, max_range, iterations, possible_keys):
		global random_notes
		infile = open("sheets/blank.ly", "r")
		data = infile.read()
		infile.close()
		# random_notes = [randint(min_range, max_range) for i in range(iterations)]
		random_notes = []
		while len(random_notes) < 100:
			random_note = randint(min_range, max_range)
			if len(random_notes) >= 1 and random_note != random_notes[-1] and (random_note % 12) in possible_keys:
					random_notes.append(random_note)
			elif len(random_notes) == 0 and (random_note % 12) in possible_keys:
					random_notes.append(random_note)

		pitch_name = [get_pitch_name(i) for i in random_notes]
		ly_notes = [self.midi_to_lilypond(i) for i in random_notes]
		for i, k in enumerate(pitch_name):
			print(pitch_name[i], ly_notes[i])

		sheets = []
		counter = 0
		for random_note in random_notes:
			ly_note = self.midi_to_lilypond(random_note)
			if random_note >= 60: # RH
				new_sheet = data.replace("NOTE_TREBLE", ly_note)
				new_sheet = new_sheet.replace("NOTE_BASS", "s4")
			else: # LH
				new_sheet = data.replace("NOTE_BASS", ly_note)
				new_sheet = new_sheet.replace("NOTE_TREBLE", "s4")
			counter += 1
			sheets.append(new_sheet)
		return sheets

	def write_sheets(self, sheets):
		for i, sheet in enumerate(sheets):
			out_file = open(f"sheets/note{i + 1}.ly", "w")
			out_file.write(sheet)
			out_file.close()


	def create_random_sheets(self, iterations):
		name_list = [f"sheets/note{i + 1}.ly" for i in range(iterations)]
		names = " ".join(name_list)
		# print(names)
		os.system(f'lilypond -fpng -dpng-width=175 -dpng-height=175 --silent {names}')
		os.system(f"move *.png notes/")		




class QuizPanel(wx.Panel):
	def __init__(self, parent):
		global random_notes
		super().__init__(parent)
		pygame.midi.init()

		self.parent = parent
		self.counter = 1
		self.total = 100

		input_id = None
		midi_found = True

		for i in range(pygame.midi.get_count()):
			if pygame.midi.get_device_info(i)[2]:
				input_id = i
				break
		if input_id is None:
			print("No MIDI input devices found.")
			pygame.midi.quit()
			midi_found = False

			if midi_found:
				print(f"Using MIDI input device: {pygame.midi.get_device_info(input_id)[1].decode()}")

		# note = get_random_note()
		# print(f"please play {note}")

		pygame.midi.init()
		self.midi_input = pygame.midi.Input(input_id)


		parent.SetTitle(f"{self.counter}/{self.total}")

		self.main_sizer = wx.BoxSizer(wx.VERTICAL)

		image = wx.Image("notes/note1.png", wx.BITMAP_TYPE_PNG)
		image.Rescale(500, 500)
		image.ConvertToBitmap()
		self.image_ctrl = wx.StaticBitmap(self, bitmap=image)
	
		self.main_sizer.Add(self.image_ctrl, flag=wx.ALL | wx.CENTER)

		self.counter_button = wx.Button(self, label="Increment Counter")
		self.counter_button.Bind(wx.EVT_BUTTON, self.increment_counter)
		self.main_sizer.Add(self.counter_button, flag=wx.ALL | wx.CENTER)

		self.SetSizer(self.main_sizer)
		self.Update()

		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.check_midi_input, self.timer)
		self.timer.Start(1) 

	def check_midi_input(self, event):
		"""Check for MIDI input periodically."""
		midi_events = 0
		if self.midi_input and self.midi_input.poll():
			midi_events = self.midi_input.read(10)
		if midi_events:
			for event in midi_events:
				data, timestamp = event
				status, note, velocity, _ = data
				if status == 144 and velocity > 0:  # Note On event
					if note == random_notes[self.counter - 1]:
						print(get_pitch_name(note))
						wx.CallAfter(self.increment_counter)
		# midi_input.close()
		# pygame.midi.quit()


	def increment_counter(self):
		if self.counter < 100:
			self.counter += 1
			self.parent.SetTitle(f"{self.counter}/{self.total}")
			image = wx.Image(f"notes/note{self.counter}.png", wx.BITMAP_TYPE_PNG)
			image.Rescale(500, 500)
			image.ConvertToBitmap()
			self.image_ctrl.SetBitmap(image)
			self.Update()
	

class MainFrame(wx.Frame):
	def __init__(self):
		super().__init__(None, title="Learning Notes", size=(500, 500))
		self.panel1 = InitialPanel(self, self.switch_to_second_screen)
		self.panel2 = None
		self.Show()
	
	def switch_to_second_screen(self):
		self.panel1.Destroy()
		self.panel2 = QuizPanel(self)
		self.Layout()

def list_midi_devices():
	"""
	List all available MIDI devices.
	"""
	pygame.midi.init()
	for i in range(pygame.midi.get_count()):
		info = pygame.midi.get_device_info(i)
		device_type = "Input" if info[2] else "Output"
		print(f"{i}: {info[1].decode()} ({device_type})")
	pygame.midi.quit()


	
	


	
if __name__ == "__main__":
	app = wx.App(False)
	frame = MainFrame()
	app.MainLoop()