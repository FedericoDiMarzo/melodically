"""
Musical notes.

This list defines, the musical notes in western notation.
The position of each notes in the list reflects the midi ordering.
"""
musical_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


def parse_midi_note(midi_note):
    """
    Function that parses a midi note into a musical note.

    :param midi_note: midi note number
    :return: musical note
    """
    return musical_notes[midi_note % 12]
