from random import randint, choice
import os

keys = [['c'], ['cis', 'des'], ['d'], ['dis', 'ees'], ['e', 'fes'], ['f', 'eis'], ['fis', 'ges'], ['g'], ['gis', 'aes'], ['a'], ['ais', 'bes'], ['b', 'ces']]
res_form = lambda x: keys[x % 12]
octave_designation_form = lambda x: ((x - 11) // 12)
get_pitch_name = lambda x: f"{choice(res_form(x))}{octave_designation_form(x)}"

def midi_to_lilypond(note):
	tone = choice(res_form(note))
	octave_destination = octave_designation_form(note)
	dist = octave_destination - 3
	return tone + dist * '\'' + (-dist) * ','

def create_new_note_file(min_range, max_range, iterations):
	infile = open("sheets/blank.ly", "r")
	data = infile.read()
	infile.close()
	# random_notes = [randint(min_range, max_range) for i in range(iterations)]
	random_notes = [i for i in range(21, 108 + 1)]
	pitch_name = [get_pitch_name(i) for i in random_notes]
	ly_notes = [midi_to_lilypond(i) for i in random_notes]
	for i, k in enumerate(pitch_name):
		print(pitch_name[i], ly_notes[i])
	# a = a + b
	sheets = []
	options = "abcdefg"
	counter = 0
	for random_note in random_notes:
		ly_note = midi_to_lilypond(random_note)
		if random_note >= 60: # RH
			new_sheet = data.replace("NOTE_TREBLE", ly_note)
			new_sheet = new_sheet.replace("NOTE_BASS", "r4")
		else: # LH
			new_sheet = data.replace("NOTE_BASS", ly_note)
			new_sheet = new_sheet.replace("NOTE_TREBLE", "r4")
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
	os.system(f'lilypond -fpng -dpng-width=175 -dpng-height=175 {names}')
	os.system(f"move *.png notes/")

iterations = 88

sheets = create_new_note_file(30, 50, iterations)
write_sheets(sheets)
create_random_sheets(iterations)
