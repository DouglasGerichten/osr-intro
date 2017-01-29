import pretty_midi

def compute_pitch_histogram(filename):
	"""Compute weighted pitch counts over a MIDI file.

	Parameters
	----------
	filename : str
		Path to a midi file on disk.

	Returns
	-------
	counts: dict
		Pitch counts over the file, keyed by pitch class.
	"""
	midi = pretty_midi.PrettyMIDI(filename)
	pitch_counts = {pc: 0 for pc in range(12)}

	for inst in midi.instruments:
			if inst.is_drum:
				continue
			for note in inst.notes:
				pc = note.pitch % 12
				pitch_counts[pc] += (note.end - note.start)
	return pitch_counts