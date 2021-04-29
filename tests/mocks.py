from abstract_melody_parser.rhythmic_parser import MidiNoteQueue
midiNoteQueueMock = [
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

midiNoteQueue = MidiNoteQueue()
for msg in midiNoteQueueMock:
    midiNoteQueue.push(msg)
