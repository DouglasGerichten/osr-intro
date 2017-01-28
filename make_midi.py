import argparse
import pretty_midi



def rando_midi(filename):
    # Create a PrettyMIDI object
    cello_c_chord = pretty_midi.PrettyMIDI()
    # Create an Instrument instance for a cello instrument
    cello_program = pretty_midi.instrument_name_to_program('Cello')
    cello = pretty_midi.Instrument(program=cello_program)
    # Iterate over note names, which will be converted to note number later
    for note_name in ['F4', 'A5', 'C5']:
        # Retrieve the MIDI note number for this note name
        note_number = pretty_midi.note_name_to_number(note_name)
        # Create a Note instance for this note, starting at 0s and ending at .5s
        note = pretty_midi.Note(velocity=100, pitch=note_number, start=0, end=2)        
        # Add it to our cello instrument
        cello.notes.append(note)
    for note_name in ['C5', 'E5', 'G5']:
        # Retrieve the MIDI note number for this note name
        note_number = pretty_midi.note_name_to_number(note_name)
        # Create a Note instance for this note, starting at 0s and ending at .5s
        note = pretty_midi.Note(velocity=100, pitch=note_number, start=2, end=4)
        # Add it to our cello instrument
        cello.notes.append(note)
    # Add the cello instrument to the PrettyMIDI object
    cello_c_chord.instruments.append(cello)

    # Write out the MIDI data
    cello_c_chord.write(filename)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filename", type=str,
        help="Filename for the output MIDI")

    args = parser.parse_args()
    rando_midi(args.filename)