import pytest
import os

import make_midi


def test_rando_midi(tmpdir):
    fout = os.path.join(str(tmpdir), "test_rando_midi_out.mid")
    make_midi.rando_midi(fout)
    assert os.path.exists(fout)