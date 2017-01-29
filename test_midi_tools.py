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
	pitch_counts = midi_tools.compute_pitch_histogram(sample_midis[0])
	assert sum(pitch_counts.values()) > 0