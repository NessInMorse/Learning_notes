from random import randint
import os

def create_new_note_file(min_range, max_range, iterations):
	infile = open("sheets/blank.ly", "r")
	data = infile.read()
	infile.close()
	random_notes = [randint(min_range, max_range) for i in range(iterations)]
	sheets = []
	options = "abcdefg"
	counter = 0
	for random_note in random_notes:
		# ly_note = midi_to_lilypond(random_note)
		# if random_note >= 60: # RH
		new_sheet = data.replace("NOTE_TREBLE", options[counter % 7])
		new_sheet = new_sheet.replace("NOTE_BASS", "")
		# new_sheet = data.replace("NOTE_BASS", "")
		# else: # LH
			# new_sheet = data.replace("NOTE_BASS", ly_note)
		counter += 1
		sheets.append(new_sheet)
	return sheets

def write_sheets(sheets):
	for i, sheet in enumerate(sheets):
		out_file = open(f"sheets/note{i + 1}.ly", "w")
		out_file.write(sheet)
		out_file.close()


def create_random_sheets(iterations):
	name_list = [f"sheets/note{i + 1}.ly" for i in range(iterations)]
	names = " ".join(name_list)
	print(names)
	os.system(f'lilypond -fpng -dpng-width=175 -dpng-height=120 {names}')
	os.system(f"move *.png notes/")

iterations = 100

sheets = create_new_note_file(30, 50, iterations)
write_sheets(sheets)
create_random_sheets(iterations)
