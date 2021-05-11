from abstract_melody_parser.harmony import musical_notes, std_to_midi, midi_to_std, mode_signatures
import numpy as np

"""
Dictionary containing, for each chord, 
another dictionary that indicates 
the color tones (c) and the chord tones (l).
"""
chord_tones = {}


def get_chord_tones(chord_dict):
    # TODO: test
    # TODO: add minor and dominant chords
    """
    Adds all the major (XM) / minor (Xm) / dominant (X7)
    chords to the chord dictionary.

    :param chord_dict: chord dictionary
    :return: the updated chord dictionary
    """
    for root in musical_notes:
        # 0 -> XM (major) ; 4 -> X7 (dominant); 5 -> Xm (minor)
        for shift in [0, 4, 5]:
            # root in std notation
            root_midi = std_to_midi(root)

            # getting the indices of chord (c) and color (l) tones
            chord_tones_indices = [0, 2, 4]  # I III V
            color_tones_indices = [i for i in range(7) if i not in chord_tones_indices]

            # applying a cumulative sum to the diatonic scale intervals
            # circular shift used to switch from major, minor and dominant (np.roll)
            # [2, 2, 1, 2, 2, 2, 1] => [0, 2, 4, 5, 7, 9, 11]
            m0 = list(np.roll(mode_signatures[0], -1 * shift))
            diatonic_scale_absolute_intervals = [sum(m0[0:i]) for i, value in enumerate(m0)]

            # getting two lists of notes in std notation for c and l
            c_tones = [midi_to_std(root_midi + diatonic_scale_absolute_intervals[i]) for i in chord_tones_indices]
            l_tones = [midi_to_std(root_midi + diatonic_scale_absolute_intervals[i]) for i in color_tones_indices]

            # dominant chords have the VII in the chord tones
            if shift == 4:
                c_tones.append(l_tones.pop(3))

            # choosing the suffix
            if shift == 0:
                suffix = 'M'
            elif shift == 4:
                suffix = '7'
            else:
                suffix = 'm'

            chord_dict[root + suffix] = {
                'c': c_tones,
                'l': l_tones
            }

    return chord_dict


# adding major, minor and dominant chords to the dictionary
# TODO: check
chord_tones = get_chord_tones(chord_tones)
