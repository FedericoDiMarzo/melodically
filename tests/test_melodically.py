import unittest
from melodically import *
from mocks import *


class TestParseMidiToStd(unittest.TestCase):
    def test_f_minus_1(self):
        self.assertEqual(midi_to_std(5), 'F')

    def test_d1(self):
        self.assertEqual(midi_to_std(26), 'D')

    def test_c4(self):
        self.assertEqual(midi_to_std(60), 'C')

    def test_f_diesis_9(self):
        self.assertEqual(midi_to_std(126), 'F#')


class TestStdToMidi(unittest.TestCase):
    def test_A_diesis(self):
        self.assertEqual(10, std_to_midi('A#'))

    def test_Ab(self):
        self.assertEqual(8, std_to_midi('Ab'))

    def test_C_diesis4(self):
        self.assertEqual(61, std_to_midi('C#', 4))

    def test_Gb0(self):
        self.assertEqual(18, std_to_midi('Gb', 0))


class TestChordToMidi(unittest.TestCase):
    def test_C7_oct5(self):
        self.assertEqual([72, 76, 79, 82], chord_to_midi('C7', 5))

    def test_A_diesis_m_oct123(self):
        self.assertEqual([34, 37, 53], chord_to_midi('A#m', [1, 2, 3]))

    def test_GM_545(self):
        self.assertEqual([79, 71, 74], chord_to_midi('GM', [5, 4, 5]))


class TestParseMusicalNote(unittest.TestCase):
    def test_E_CM(self):
        self.assertEqual(parse_musical_note('E', 'CM'), 'c')

    def test_B_CM(self):
        self.assertEqual(parse_musical_note('B', 'CM'), 'l')

    def test_B_diesis_CM(self):
        self.assertEqual(parse_musical_note('B#', 'CM'), 'x')


class TestGetDurations(unittest.TestCase):
    def test_60bpm(self):
        rhythmic_dictionary = get_durations(60)
        self.assertAlmostEqual(rhythmic_dictionary['1'], 4)
        self.assertAlmostEqual(rhythmic_dictionary['2'], 2)
        self.assertAlmostEqual(rhythmic_dictionary['4'], 1)
        self.assertAlmostEqual(rhythmic_dictionary['4dot'], 3 / 2)
        self.assertAlmostEqual(rhythmic_dictionary['4t'], 2 / 3)
        self.assertAlmostEqual(rhythmic_dictionary['8'], 1 / 2)
        self.assertAlmostEqual(rhythmic_dictionary['8t'], 1 / 3)
        self.assertAlmostEqual(rhythmic_dictionary['16'], 1 / 4)
        self.assertAlmostEqual(rhythmic_dictionary['16t'], 1 / 6)


class TestMidiNoteQueue(unittest.TestCase):
    def test_mock_1_0(self):
        self.assertEqual(midi_note_queue_1.pop(), midi_note_queue_mock_1[0])

    def test_mock_1_1(self):
        self.assertEqual(midi_note_queue_1.pop(), midi_note_queue_mock_1[1])

    def test_mock_1_2(self):
        self.assertEqual(midi_note_queue_1.pop(), midi_note_queue_mock_1[2])

    def test_mock_1_3(self):
        self.assertEqual(midi_note_queue_1.pop(), midi_note_queue_mock_1[3])

    def test_mock_1_4(self):
        self.assertEqual(midi_note_queue_1.pop(), midi_note_queue_mock_1[4])

    def test_mock_1_5(self):
        self.assertEqual(midi_note_queue_1.pop(), midi_note_queue_mock_1[5])

    def test_mock_1_6(self):
        self.assertEqual(midi_note_queue_1.pop(), midi_note_queue_mock_1[8])

    def test_mock_2_0(self):
        self.assertEqual(midi_note_queue_2.pop(), midi_note_queue_mock_2[2])

    def test_mock_2_1(self):
        self.assertEqual(midi_note_queue_2.pop(), midi_note_queue_mock_2[3])

    def test_clear(self):
        midi_queue = MidiNoteQueue()
        for msg in midi_note_queue_mock_3:
            midi_queue.push(msg['type'], msg['note'], msg['timestamp'])
        midi_queue.clear()
        self.assertEqual([], midi_queue.get_container())

    def test_get_notes(self):
        midi_queue = MidiNoteQueue()
        for msg in midi_note_queue_mock_2:
            midi_queue.push(msg['type'], msg['note'], msg['timestamp'])
        midi_queue.clean_unclosed_note_ons()
        self.assertEqual(['A#'], midi_queue.get_notes())


class TestGetNearestRhythm(unittest.TestCase):
    def setUp(self):
        self.durations = get_durations(60)

    def test_0(self):
        self.assertEqual('1', get_nearest_rhythm(8, self.durations))

    def test_1(self):
        self.assertEqual('1', get_nearest_rhythm(4, self.durations))

    def test_2(self):
        self.assertEqual('4dot', get_nearest_rhythm(3 / 2 + 0.01, self.durations))

    def test_3(self):
        self.assertEqual('4dot', get_nearest_rhythm(3 / 2 - 0.02, self.durations))

    def test_4(self):
        self.assertEqual('16t', get_nearest_rhythm(0.001, self.durations))

    def test_5(self):
        self.assertEqual('16', get_nearest_rhythm(1 / 4 - 0.02, self.durations))


class TestParseRhythm(unittest.TestCase):
    def setUp(self):
        self.durations = get_durations(60)
        self.midi_queue = MidiNoteQueue()
        for msg in midi_note_queue_mock_3:
            self.midi_queue.push(msg['type'], msg['note'], msg['timestamp'])

    def test_0(self):
        result = parse_rhythm(self.midi_queue, self.durations)
        self.assertEqual(['1', '16', '4'], result)

    def test_1(self):
        self.midi_queue.clear()
        for msg in midi_note_queue_mock_4:
            self.midi_queue.push(msg['type'], msg['note'], msg['timestamp'])
        result = parse_rhythm(self.midi_queue, self.durations)
        self.assertEqual(['1', '16', 'r16', '4'], result)


class TestParseMelody(unittest.TestCase):
    def setUp(self):
        self.durations = get_durations(60)
        self.midi_queue = MidiNoteQueue()
        for msg in midi_note_queue_mock_4:
            self.midi_queue.push(msg['type'], msg['note'], msg['timestamp'])

    def test_0(self):
        result = parse_melody(self.midi_queue, 'CM', self.durations)
        self.assertEqual(['l1', 'c16', 'r16', 'c4'], result)


class TestHarmonicState(unittest.TestCase):
    def setUp(self):
        self.hstate = HarmonicState(8)

    def test_C_ionic(self):
        notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C']
        self.hstate.push_notes(notes)
        self.assertEqual(modes_dict['C'][0][0], self.hstate.get_mode_notes())

    def test_A_locrian(self):
        notes = ['A', 'A#', 'C', 'D', 'D#', 'F', 'G', 'A']
        self.hstate.push_notes(notes)
        self.assertEqual(modes_dict['A'][0][6], self.hstate.get_mode_notes())

    def test_A_eolian(self):
        notes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'A']
        self.hstate.push_notes(notes)
        self.assertEqual(modes_dict['A'][0][5], self.hstate.get_mode_notes())


class TestSequenceFitsMeasures(unittest.TestCase):
    def test_sequence1(self):
        sequence = ['4', '4', '4', '4']
        self.assertEqual(True, sequence_fits_measures(sequence, 1))

    def test_sequence2(self):
        sequence = ['4', '4', '4', '4', '16']
        self.assertEqual(False, sequence_fits_measures(sequence, 1))

    def test_sequence3(self):
        sequence = ['16', '16', '8', '4', '4', '16']
        self.assertEqual(True, sequence_fits_measures(sequence, 1))

    def test_sequence4(self):
        sequence = ['16', '16', '8', '4', '4', '8', '8']
        self.assertEqual(True, sequence_fits_measures(sequence, 1))

    def test_sequence5(self):
        sequence = ['16', '16', '8', '4', '4', '8', '8', '16']
        self.assertEqual(False, sequence_fits_measures(sequence, 1))

    def test_sequence7(self):
        sequence = ['1', '1', '1', '1']
        self.assertEqual(True, sequence_fits_measures(sequence, 4))

    def test_sequence8(self):
        sequence = ['8t', '8t', '8t', '8t', '8t', '8t', '8t', '8t', '8t']
        self.assertEqual(True, sequence_fits_measures(sequence, 1))

    def test_sequence9(self):
        sequence = ['r1']
        self.assertEqual(True, sequence_fits_measures(sequence, 1))


class TestClipRhythmicSequence(unittest.TestCase):
    def test_sequence1(self):
        sequence = ['1', '1', '1r', '1']
        self.assertEqual(['1', '1', '1r'], clip_rhythmic_sequence(sequence, 3))

    def test_sequence2(self):
        sequence = ['8', '8', '4', '4', '4', '16t']
        self.assertEqual(['8', '8', '4', '4', '4'], clip_rhythmic_sequence(sequence, 1))

    def test_sequence3(self):
        sequence = ['1', '1', '1', '1']
        self.assertEqual(['1', '1', '1', '1'], clip_rhythmic_sequence(sequence, 4))

    def test_sequence4(self):
        sequence = ['1']
        self.assertEqual(['1'], clip_rhythmic_sequence(sequence, 1))

    def test_sequence5(self):
        sequence = ['1', '1', '1', '1']
        clip_rhythmic_sequence(sequence, 1)
        self.assertEqual(['1', '1', '1', '1'], sequence)


if __name__ == '__main__':
    unittest.main()
