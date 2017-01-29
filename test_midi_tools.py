import pytest
#glob takes wildcard and matches things against it
import glob
import os

import midi_tools

@pytest.fixture()
def sample_midis():
	midi_fmt = os.path.join(os.path.dirname(__file__), 'data', "*.mid")
	return glob.glob(midi_fmt)

def test_compute_pitch_histogram(sample_midis):
	# for dictionaries, you can use keys and values
	data = midi_tools.compute_pitch_histogram(sample_midis[0])
	# test that 'name' is a key in 'data'
	assert 'name' in data
	# test that the pitch histogram values sum to more than 0
	assert sum(data['pitches'].values()) > 0

def test_process_many(sample_midis):
	results = midi_tools.process_many(sample_midis, n_jobs=-2, verbose=50)
	assert len(results) == len(sample_midis)