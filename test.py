import pygame.midi
from random import choice, randint

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

def main():
	pygame.midi.init()

	input_id = None
	midi_found = True

	keys = ['C', 'C# | D♭', 'D', 'D# | E♭', 'E | F♭', 'F | E#', 'F# | G♭', 'G', 'G# | A♭', 'A', 'A# | B♭', 'B | C♭']
	res_form = lambda x: keys[x % 12]
	octave_designation_form = lambda x: ((x - 12) // 12)
	get_pitch_name = lambda x: f"{res_form(x)}{octave_designation_form(x)}"

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

		midi_input = pygame.midi.Input(input_id)

		random_notes = [randint(71, 71) for i in range(5)]
		current_note = 0
		counter = 0

		try:
			print("Listening for MIDI input...")
			while True:

				if not counter:
					print(f"Please hit strike {get_pitch_name(random_notes[current_note])}")
					counter += 1


				if midi_input.poll(): # Check if data coming in
					midi_events = midi_input.read(10)
					for event in midi_events:
						data, timestamp = event
						status, note, velocity, _ = data
						if status == 144 and velocity > 0: # Note On event
							if note == random_notes[current_note]:
								print("Yeeeeet")
								if current_note == len(random_notes) - 1:
									print("Congratulations, you finished!")
								else:
									counter = 0
									current_note += 1
							# print(f"Note ON: {note} {keys[res_form(note)]}{octave_designation_form(note)} (Velocity: {velocity})")
							# print(f"{keys[res_form(note)]}{octave_designation_form(note)}")
						elif status == 128 or (status == 144 and velocity == 0): # Note Off event
							pass
							# print(f"Note OFF: {note}")
		except KeyboardInterrupt:
			print("\nExiting MIDI listener.")
	
	midi_input.close()
	pygame.midi.quit()

def get_random_note():
	key = choice("ABCDEFG")
	num = randint(3, 5)
	return f"{key}{num}"



if __name__ == "__main__":
	print("Available MIDI devices:")
	list_midi_devices()
	main()






