import unittest
from parser.parser import musical_notes, parse_midi_note


class TestParse(unittest.TestCase):
    def test_f_minus_1(self):
        self.assertEqual(parse_midi_note(5), 'F')

    def test_d1(self):
        self.assertEqual(parse_midi_note(26), 'D')

    def test_c4(self):
        self.assertEqual(parse_midi_note(60), 'C')

    def test_f_diesis_9(self):
        self.assertEqual(parse_midi_note(126), 'F#')


if __name__ == '__main__':
    unittest.main()
