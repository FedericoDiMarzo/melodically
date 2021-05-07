def get_durations(bpm):
    """
    Function that generate a dictionary containing
    the duration in seconds of various rhythmic figures.

    :param bpm: beat per minutes
    :return: rhythmic dictionary
    """
    beat_time = 60 / bpm
    return {
        '1': beat_time * 4,
        '2': beat_time * 2,
        '4': beat_time * 1,
        '4dot': beat_time * 3 / 2,
        '4t': beat_time * 2 / 3,
        '8': beat_time * 1 / 2,
        '8t': beat_time * 1 / 3,
        '16': beat_time * 1 / 4,
        '16t': beat_time * 1 / 6,
    }


def get_nearest_rhythm(interval, rhythmical_durations):
    """
    Given a certain interval in seconds, gets the rhythmical duration
    that has the lower distance with it.

    :param interval: duration in seconds
    :param rhythmical_durations: dictionary returned by the get_durations
    :return:
    """

    # the keys and the values obtained from the methods "values" and "keys"
    # of a dictionary are correctly ordered, so we can calculate
    # the distances from the keys, get the index of the argmin
    # and use it to get the correct key

    # values of the rhythmical_durations dictionary
    rhythmical_durations_values = list(rhythmical_durations.values())

    # keys of the rhythmical_durations dictionary
    rhythmical_durations_keys = list(rhythmical_durations.keys())

    # list comprehension used to map the distance function to the values
    distances = [abs(interval - x) for x in rhythmical_durations_values]

    # argmin of the distance (an index)
    result_index = distances.index(min(distances))

    # using the index to get the correct rhythmical duration key
    return rhythmical_durations_keys[result_index]


def parse_rhythm(midi_queue, rhythmical_durations):
    """
    Parse a midi
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
