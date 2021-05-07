from abstract_melody_parser.chords import chord_tones

"""
Musical notes.

This list defines, the musical notes in western notation.
The position of each notes in the list reflects the midi ordering.
"""
musical_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

"""
Musical notes with the flat notation
"""
musical_notes_b = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']


def parse_midi_note(midi_note):
    """
    Function that parses a midi note into a musical note.

    :param midi_note: midi note number
    :return: musical note
    """
    return musical_notes[midi_note % 12]


# TODO: test this function
def musical_note_to_midi(musical_note, octave=-1):
    """
    Convert a musical note into a midi note.

    :param musical_note: musical note symbol
    :param octave: octave of the note
    :return: midi note number
    """
    octave_offset = (octave + 1) * 12
    if musical_note in musical_notes:
        return musical_notes.index(musical_note) + octave_offset
    else:
        return musical_notes_b.index(musical_note) + octave_offset


def parse_musical_note(musical_note, chord):
    """
    Function that given a chord, parses a musical note
    into an abstract melody_parser notation.

    :param musical_note: standard note notation
    :param chord: chord notation
    :return: abstract melody_parser note
    """
    if musical_note in chord_tones[chord]['c']:
        return 'c'
    elif musical_note in chord_tones[chord]['l']:
        return 'l'
    else:
        return 'x'
