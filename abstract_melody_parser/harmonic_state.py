from abstract_melody_parser.harmony import midi_to_std, get_root, harmonic_affinities, modes_dict


class HarmonicState:
    """
    This class allows to monitor and update an internal harmonic state,
    influenced by external notes inputs
    """

    def __init__(self, buffer_size=16):
        # contains the input notes in std notation
        self.noteBuffer = []

        # max size of the buffer
        self.bufferSize = buffer_size

        # mode dictionary used to represent a modal scale
        # root: root note of the scale
        # mode_signature_index: index of the interval scheme of a modal scale
        # mode_index: index of the mode inside a certain interval scheme
        self.currentMode = {'root': 'C', 'mode_signature_index': 0, 'mode_index': 0}

    def push_notes(self, new_notes):
        """
        Pushes new note inside the buffer.
        If the buffer overflows, the older notes are discarded.

        :param new_notes: list of new notes
        """
        self.noteBuffer = self.noteBuffer + new_notes
        while len(self.noteBuffer) > self.bufferSize:
            self.noteBuffer.pop(0)  # removing old notes

    def update_scale(self):
        """
        Updates the currentMode attribute based on the notes in the buffer,
        applying the harmonic_affinities function to them.

        :return: currentMode
        """
        notes_std = [n for n in self.noteBuffer]
        root = get_root(notes_std)
        modes_affinities = harmonic_affinities(root, notes_std)
        mode_signature_index = modes_affinities.index(max(modes_affinities))
        tmp = modes_affinities[mode_signature_index]  # sequence with the lowest distance
        mode_index = tmp.index(max(tmp))

        self.currentMode['root'] = root
        self.currentMode['mode_signature_index'] = mode_signature_index
        self.currentMode['mode_index'] = mode_index

        return self.currentMode

    def get_mode_notes(self):
        """
        Gets the current notes of the current modal scale.

        :return: list of notes of the current modal scale
        """
        self.update_scale()
        tmp = modes_dict[self.currentMode['root']]
        tmp = tmp[self.currentMode['mode_signature_index']]
        return tmp[self.currentMode['mode_index']]
