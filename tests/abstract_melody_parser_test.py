import unittest
from abstract_melody_parser.melody_parser import parse_midi_note, parse_musical_notes
from abstract_melody_parser.rhythmic_parser import get_durations, get_nearest_rhythm
from mocks import midiNoteQueueMock1, midiNoteQueueMock2, midiNoteQueue1, midiNoteQueue2


class TestParseMidiNote(unittest.TestCase):
    def test_f_minus_1(self):
        self.assertEqual(parse_midi_note(5), 'F')

    def test_d1(self):
        self.assertEqual(parse_midi_note(26), 'D')

    def test_c4(self):
        self.assertEqual(parse_midi_note(60), 'C')

    def test_f_diesis_9(self):
        self.assertEqual(parse_midi_note(126), 'F#')


class TestParseMusicalNote(unittest.TestCase):
    def test_R_CM(self):
        self.assertEqual(parse_musical_notes('R', 'CM'), 'r')

    def test_E_CM(self):
        self.assertEqual(parse_musical_notes('E', 'CM'), 'c')

    def test_B_CM(self):
        self.assertEqual(parse_musical_notes('B', 'CM'), 'l')

    def test_B_diesis_CM(self):
        self.assertEqual(parse_musical_notes('B#', 'CM'), 'x')


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
        self.assertEqual(midiNoteQueue1.pop(), midiNoteQueueMock1[0])

    def test_mock_1_1(self):
        self.assertEqual(midiNoteQueue1.pop(), midiNoteQueueMock1[1])

    def test_mock_1_2(self):
        self.assertEqual(midiNoteQueue1.pop(), midiNoteQueueMock1[2])

    def test_mock_1_3(self):
        self.assertEqual(midiNoteQueue1.pop(), midiNoteQueueMock1[3])

    def test_mock_1_4(self):
        self.assertEqual(midiNoteQueue1.pop(), midiNoteQueueMock1[4])

    def test_mock_1_5(self):
        self.assertEqual(midiNoteQueue1.pop(), midiNoteQueueMock1[5])

    def test_mock_1_6(self):
        self.assertEqual(midiNoteQueue1.pop(), midiNoteQueueMock1[8])

    def test_mock_2_0(self):
        self.assertEqual(midiNoteQueue2.pop(), midiNoteQueueMock2[1])

    def test_mock_2_1(self):
        self.assertEqual(midiNoteQueue2.pop(), midiNoteQueueMock2[2])


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
        self.assertEqual('16', get_nearest_rhythm(1/4-0.02, self.durations))


if __name__ == '__main__':
    unittest.main()
