from abstract_melody_parser.rhythmic_parser import MidiNoteQueue

midiNoteQueueMock1 = [
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

midiNoteQueueMock2 = [
    # an unclosed note on
    {
        'type': 'note_on',
        'note': 75,
        'timestamp': 40
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

midiNoteQueue1 = MidiNoteQueue()
for msg in midiNoteQueueMock1:
    midiNoteQueue1.push(msg)

midiNoteQueue2 = MidiNoteQueue()
for msg in midiNoteQueueMock2:
    midiNoteQueue2.push(msg)
midiNoteQueue2.clean_unclosed_note_ons()
