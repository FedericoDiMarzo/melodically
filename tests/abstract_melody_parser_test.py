import unittest
from abstract_melody_parser.melody_parser import parse_midi_note, parse_musical_notes
from abstract_melody_parser.rhythmic_parser import get_durations


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
    def simple_test(self):
        rhythmic_dictionary = get_durations(1)
        self.assertAlmostEqual(rhythmic_dictionary['1'], 4)
        self.assertAlmostEqual(rhythmic_dictionary['2'], 2)
        self.assertAlmostEqual(rhythmic_dictionary['4'], 1)
        self.assertAlmostEqual(rhythmic_dictionary['4dot'], 3 / 2)
        self.assertAlmostEqual(rhythmic_dictionary['4t'], 2 / 3)
        self.assertAlmostEqual(rhythmic_dictionary['8'], 1 / 2)
        self.assertAlmostEqual(rhythmic_dictionary['8t'], 1 / 3)
        self.assertAlmostEqual(rhythmic_dictionary['16'], 1 / 4)
        self.assertAlmostEqual(rhythmic_dictionary['16t'], 1 / 6)


if __name__ == '__main__':
    unittest.main()
