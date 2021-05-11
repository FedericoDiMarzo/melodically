import numpy as np
from collections import Counter

"""
Musical notes.

This list defines, the musical notes in standard (std) notation.
The position of each notes in the list reflects the midi ordering.
"""
musical_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

"""
Musical notes with the flat notation
"""
musical_notes_b = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']

"""
this data structure contains all the
possible semitone sequences to construct
many families of modal scales
"""
mode_signatures = [
    [2, 2, 1, 2, 2, 2, 1],  # TTSTTTS
    # [2, 2, 1, 3, 1, 2, 1],
]


def midi_to_std(midi_note):
    """
    Function that parses a midi note into a musical note in std notation.

    :param midi_note: midi note number
    :return: musical note
    """
    return musical_notes[midi_note % 12]


def std_to_midi(musical_note, octave=-1):
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


def get_root(notes):
    """
    returns the most common value in the list of notes

    :param notes: notes in standard notation
    :return: single note in standard notation
    """
    return max(set(notes), key=notes.count)


def get_all_modes(root):
    """
    given a root, calculates all the modes

    :param root: note in std notation
    :return: multi dimensional list of size [len(mode_signatures)x7x7] containing the modes
    """
    modes_note_std = []
    for i in range(len(mode_signatures)):  # iterating for different modes families
        modes_note_std.append([])
        current_sequence = np.array(mode_signatures[i])
        for j in range(7):  # iterating for each mode in the family
            modes_note_std[i].append([root])
            last_note = musical_notes.index(root)
            for k in range(6):  # iterating for each note in the scale
                last_note = (last_note + current_sequence[k]) % 12
                modes_note_std[i][j].append(musical_notes[last_note])
            current_sequence = np.roll(current_sequence, -1)  # circular shift of the note sequence
    return modes_note_std


"""
dictionary containing all the notes as keys and
the respective modes as value
"""
modes_dict = {root: get_all_modes(root) for root in musical_notes}


def harmonic_affinities(root, notes_std):
    """
    Given a root and a set of notes, returns a multidimensional list of the
    size of the value of the modes_dict using the root as a key, that has as elements
    the result of a distance function applied to the various notes of each modal scale.

    :param root: root note in std notation
    :param notes_std: list of target notes in std notation
    :return: multidimensional list containing harmonic distances between notes_std and the modes of root
    """

    # affinity points used for each degree of a modal scale
    positive_weights = [1, 0.5, 3, 0.2, 0.4, 2, 0.1]

    # affinity points subtracted from the notes out of scale
    negative_weight = 2

    # counting the occurrences of the input notes
    counter = Counter(notes_std)

    # bulting the multidimensional affinity list
    affinities = []
    for i in range(len(mode_signatures)):  # for each mode signature (interval structure)
        affinities.append([])
        for j in range(7):  # TODO: adapt to scale length?
            curr_mode = modes_dict[root][i][j]  # list of 7 notes
            aff = 0  # initializing the affinity
            for k in range(7):
                # calculating the positive weights
                aff = aff + counter[curr_mode[k]] * positive_weights[k]
            not_in_the_mode = [note for note in notes_std if note not in curr_mode]
            aff = aff - len(not_in_the_mode) * negative_weight
            aff = aff / len(notes_std)  # normalizing
            affinities[i].append(aff)

    return affinities
