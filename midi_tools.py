""" Compute statistics over MIDI files.

Usage
-----
# Run with default parameters
$ python midi_tools.py data/*.mid stats.json

# Run with full verbosity
$ python midi_tools.py "data/*.mid" stats.json --verbose 50

# Run with only one CPU
$ python midi_tools.py "data/*.mid" stats.json --n_jobs 1

# Run with two CPUs and a verbosity level of 20
$ python midi_tools.py "data/*.mid" stats.json --n_jobs 2 --verbose 20 
"""

import argparse
import glob
import json
from joblib import Parallel, delayed
import os
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
	
	# @ the top because these must run no matter what
	pitch_counts = {pc: 0 for pc in range(12)}
	# returns e.g. data/mymidi2.mid as "data" and "mymidi2.mid"
	name = os.path.split(filename)[-1]
	# ... but then try to do this stuff
	try:
		midi = pretty_midi.PrettyMIDI(filename)
		for inst in midi.instruments:
			if inst.is_drum:
				continue
			for note in inst.notes:
				pc = note.pitch % 12
				pitch_counts[pc] += (note.end - note.start)

	except IOError as derp:
		print("woah buddy, {} died: {}".formate(filename, derp))
		
	finally:
		# return as dictionary
		return {'name': name, 
				'pitches': pitch_counts}

#n_jobs how many cores to use. -1 is all -2 is all but one
#Parallel sets up processing pool
#parameters get passed as a dictionary for Parallel
def process_many(filenames, n_jobs, verbose):
	pool = Parallel(n_jobs=n_jobs, verbose=verbose)
	fx = delayed(compute_pitch_histogram)
	return pool(fx(fn) for fn in filenames)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filepattern", type=str,
        help="Filepattern for finding MIDI files, e.g. 'data/*.mid'")
    parser.add_argument(
        "output_file", type=str,
        help="Output file for writing results, r.h. 'data.json'")
    parser.add_argument(
    	#--for optional. you must set defaults with optional arguments
        "--n_jobs", metavar='n_jobs', type=int, default=-2,
        help="Number of CPUs to use for processing.")
    parser.add_argument(
        "--verbose", metavar='verbose', type=int, default=0,
        help="Verbosity level for writing outputs.")

    args = parser.parse_args()
    # glob makes wildcards work in the correct context
    filenames = glob.glob(args.filepattern)
    results =process_many(filenames, args.n_jobs, args.verbose)
    with open(args.output_file, 'w') as fp:
    	#indent=2 is for good formating
    	json.dump(results, fp, indent=2)



