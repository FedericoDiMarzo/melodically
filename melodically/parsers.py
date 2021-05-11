from melodically.rhythm import get_nearest_rhythm
from melodically.chords import chord_tones


def parse_musical_note(musical_note, chord):
    """
    Function that given a chord, parses a musical note
    into an abstract melody_parser notation.

    ============================
    MELODIC SYMBOLS
    ============================
    c: chord tone
    l: color tone
    x: random tone
    ============================

    :param musical_note: standard note notation
    :param chord: chord notation
    :return: abstract melody_parser note
    """
    if musical_note in chord_tones[chord]['c']:
        return 'c'
    elif musical_note in chord_tones[chord]['l']:
        return 'l'
    else:
        return 'x'


def parse_rhythm(midi_queue, rhythmical_durations):
    """
    Given a MidiNoteQueue object and a rhytmical_duration dictionary,
    parses the note messages contained into the MidiNoteQueue into
    a list of the following symbols, based on the durations of the various
    notes and rests.

    ============================
    RHYTHMIC SYMBOLS
    ============================
    1: whole note
    2: half note
    4: quarter note
    4dot: quarter note dotted
    4t: quarter note triplet
    8: eight note
    8t: eight note triplet
    16: sixteenth note
    16t: sixteenth note triplet

    the rests are indicated with an "r" suffix
    ex: r4 (quarter note rest)
    ============================

    :param midi_queue: MidiNoteQueue object
    :param rhythmical_durations: dictionary of harmonic durations
    :return: list of duration symbols
    """
    result = []  # this list will contain the rhythmical symbols
    midi_queue.clean_unclosed_note_ons()
    midi_queue_container = midi_queue.get_container()
    for i in range(len(midi_queue_container)):
        if midi_queue_container[i]['type'] == 'note_on':
            j = i + 1
            # finding the corresponding subsequent note_off
            while not (midi_queue_container[j]['type'] == 'note_off' and midi_queue_container[j]['note'] ==
                       midi_queue_container[i]['note']):
                j = j + 1
            # from here on j is the index of the note_off
            interval = midi_queue_container[j]['timestamp'] - midi_queue_container[i]['timestamp']

            # getting the closest rhythmic figure and adding it to the result
            rhythm = get_nearest_rhythm(interval, rhythmical_durations)
            result.append(rhythm)

            # computing also the rest
            if i == j - 1 and j < len(midi_queue_container) - 1:
                # no other note_ons between the current note_on and note_off
                rest_interval = midi_queue_container[j + 1]['timestamp'] - midi_queue_container[j]['timestamp']
                if rest_interval >= 0.08:
                    # rhythmic figure for the rest
                    rest_rhythm = get_nearest_rhythm(interval, rhythmical_durations)
                    result.append('r' + rest_rhythm)

    return result


def parse_melody(midi_queue, chord, rhythmical_durations):
    rhythmic_symbols = parse_rhythm(midi_queue, rhythmical_durations)
    notes = midi_queue.get_notes()
    note_count = 0
    result = []
    for i in range(len(rhythmic_symbols)):
        symbol = rhythmic_symbols[i]
        if 'r' not in symbol:
            # note detected
            symbol = parse_musical_note(notes[note_count], chord) + symbol
            note_count = note_count + 1
        result.append(symbol)

    return result
