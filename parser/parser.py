from parser.chords import chord_tones

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


def parse_musical_notes(musical_note, chord):
    """
    Function that given a chord, parses a musical note
    into an abstract melody notation.

    :param musical_note: standard note notation
    :param chord: chord notation
    :return: abstract melody note
    """
    if musical_note == 'R':
        return 'r'
    if musical_note in chord_tones[chord]['c']:
        return 'c'
    elif musical_note in chord_tones[chord]['l']:
        return 'l'
    else:
        return 'x'
