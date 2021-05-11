from abstract_melody_parser.rhythm import get_nearest_rhythm
from abstract_melody_parser.chords import chord_tones


def parse_musical_note(musical_note, chord):
    """
    Function that given a chord, parses a musical note
    into an abstract melody_parser notation.

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
    # TODO: description

    :param midi_queue:
    :param rhythmical_durations:
    :return:
    """
    # TODO: parse the rests too?
    result = []  # this list will contain the rhythmical symbols
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
    return result
