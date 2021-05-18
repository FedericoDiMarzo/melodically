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


normalized_durations = get_durations(60)


# TODO: documentation
def sequence_fits_measures(rhythmic_sequence, measures):
    """
    Checks if a rhythmic sequence fits inside a certain number of 4/4 measures.

    :param rhythmic_sequence: list of rhythmical symbols
    :param measures: number of measures
    :return: True if the sequence fits the measures
    """
    rhythmic_sequence_values = [normalized_durations[key.replace('r', '')] for key in rhythmic_sequence]
    return sum(rhythmic_sequence_values) <= 4 * measures
