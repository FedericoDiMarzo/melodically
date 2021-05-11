from abstract_melody_parser.harmony import midi_to_std, get_root, harmonic_affinities, modes_dict


# TODO: comments
class HarmonicState:
    def __init__(self, buffer_size=16):
        self.noteBuffer = []
        self.bufferSize = buffer_size  # TODO: test this value
        self.currentMode = {'root': 'C', 'mode_signature_index': 0, 'mode_index': 0}

    def push_notes(self, new_notes):
        self.noteBuffer = self.noteBuffer + new_notes
        while len(self.noteBuffer) > self.bufferSize:
            self.noteBuffer.pop(0)  # removing old notes

    def change_mode(self):
        notes_std = [n for n in self.noteBuffer]
        root = get_root(notes_std)
        modes_affinities = harmonic_affinities(modes_dict[root], notes_std)
        mode_signature_index = modes_affinities.index(max(modes_affinities))
        tmp = modes_affinities[mode_signature_index]  # sequence with the lowest distance
        mode_index = tmp.index(max(tmp))

        self.currentMode['root'] = root
        self.currentMode['mode_signature_index'] = mode_signature_index
        self.currentMode['mode_index'] = mode_index

        return self.currentMode
