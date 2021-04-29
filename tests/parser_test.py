import unittest
from parser.parser import musical_notes, parse_midi_note, parse_musical_notes


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


if __name__ == '__main__':
    unittest.main()
