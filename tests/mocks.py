from abstract_melody_parser import MidiNoteQueue

# used to test the MidiQueue class
midi_note_queue_mock_1 = [
    # normal note on/off
    {
        'type': 'note_on',
        'note': 10,
        'timestamp': 10
    },

    {
        'type': 'note_off',
        'note': 10,
        'timestamp': 12
    },

    # normal note on/off but close to the last note off
    {
        'type': 'note_on',
        'note': 20,
        'timestamp': 12.02
    },

    {
        'type': 'note_off',
        'note': 20,
        'timestamp': 14
    },

    # normal note on/off but note on starts before the last note off
    {
        'type': 'note_on',
        'note': 24,
        'timestamp': 13
    },

    {
        'type': 'note_off',
        'note': 24,
        'timestamp': 13.5
    },

    # bad note off
    {
        'type': 'note_off',
        'note': 47,
        'timestamp': 20
    },

    # another bad note off
    {
        'type': 'note_off',
        'note': 60,
        'timestamp': 25
    },

    # two note on, with the second one too close with the first one
    {
        'type': 'note_on',
        'note': 70,
        'timestamp': 30
    },

    {
        'type': 'note_on',
        'note': 74,
        'timestamp': 30.01
    }
]

# used to test the MidiQueue class
midi_note_queue_mock_2 = [
    # an unclosed note on
    {
        'type': 'note_on',
        'note': 75,
        'timestamp': 20
    },

    # another unclosed note on
    {
        'type': 'note_on',
        'note': 76,
        'timestamp': 22
    },

    # an note on that is closed by a note off
    {
        'type': 'note_on',
        'note': 70,
        'timestamp': 30
    },

    {
        'type': 'note_off',
        'note': 70,
        'timestamp': 45
    },
]

# used to test rests for the parse_rhythm function
# the bpm is supposed to be 60
# correct output: ['1', '16', '4']
midi_note_queue_mock_3 = [

    # whole note
    {
        'type': 'note_on',
        'note': 65,
        'timestamp': 2 - 0.003
    },

    {
        'type': 'note_off',
        'note': 65,
        'timestamp': 6 - 0.001
    },

    # sixteenth note
    {
        'type': 'note_on',
        'note': 55,
        'timestamp': 6
    },

    {
        'type': 'note_off',
        'note': 55,
        'timestamp': 6.25 + 0.001
    },

    # quarter note
    {
        'type': 'note_on',
        'note': 75,
        'timestamp': 6.30
    },

    {
        'type': 'note_off',
        'note': 75,
        'timestamp': 7.30 + 0.02
    },
]

# used to test the parse_rhythm function
# the bpm is supposed to be 60
# correct output: ['1', '16', '16', '4']
midi_note_queue_mock_4 = [

    # whole note
    {
        'type': 'note_on',
        'note': 65,
        'timestamp': 2 - 0.003
    },

    {
        'type': 'note_off',
        'note': 65,
        'timestamp': 6 - 0.001
    },

    # sixteenth note
    {
        'type': 'note_on',
        'note': 55,
        'timestamp': 6
    },

    {
        'type': 'note_off',
        'note': 55,
        'timestamp': 6.25 + 0.001
    },

    # sixteenth note rest

    # quarter note
    {
        'type': 'note_on',
        'note': 76,
        'timestamp': 8
    },

    {
        'type': 'note_off',
        'note': 76,
        'timestamp': 9 + 0.02
    },
]

midi_note_queue_1 = MidiNoteQueue()
for msg in midi_note_queue_mock_1:
    midi_note_queue_1.push(msg)

midi_note_queue_2 = MidiNoteQueue()
for msg in midi_note_queue_mock_2:
    midi_note_queue_2.push(msg)
midi_note_queue_2.clean_unclosed_note_ons()
