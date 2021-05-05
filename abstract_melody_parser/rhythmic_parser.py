import time


def get_timestamp_msg(midi_msg_type, midi_note_value):
    """
    Function that given a note_on/off midi message returns a dictionary
    that encapsule the message with a timestamp, that can be used to determine
    the duration between a note_on and note_off message.

    :param midi_msg_type: note_on or note_off
    :param midi_note_value: midi note number
    :return: dictionary containing the midi message and a timestamp
    """
    return {
        'type': midi_msg_type,
        'note': midi_note_value,
        'timestamp': time.time()
    }


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


class MidiNoteQueue:
    """
    A midi queue containing note_on/off midi messages and timestamps
    (the data structure returned by the get_timestamp_msg function).
    This queue is used by the rhythmic parser algorithm.
    """

    def __init__(self):
        # container used to implement the queue
        self._container = []

        # timestamp of the last note_on message
        self._last_timestamp = 0

        # list of midi values of the note_on messages that are not closed yet
        self._open_note_on_list = []

        # threshold in seconds to discard notes that are too close
        self._minimum_interval = 0.06

    def push(self, midi_msg):
        """
        Pushes a note_on/off message in the queue.
        If the note_on message is too close with the last note_on, the new entry is discarded.
        If a note_off message doesn't close a note_on message, the new entry is discarded.

        :param midi_msg: dictionary returned by the get_timestamp_msg function
        """

        if midi_msg['type'] == 'note_on':  # note_on case
            # checking if the pushed note_on is too close with the last one
            if midi_msg['timestamp'] - self._last_timestamp > self._minimum_interval:
                self._open_note_on_list.append(midi_msg['note'])
                self._container.append(midi_msg)

        elif midi_msg['type'] == 'note_off':  # note_off case
            # checking if the note_off closes a note on
            if midi_msg['note'] in self._open_note_on_list:
                self._open_note_on_list.remove(midi_msg['note'])
                self._container.append(midi_msg)

        # all other types of midi messages are excluded automatically

    def pop(self):
        """
        Pops a midi message from the front of the queue.

        :return: midi message with timestamp
        """
        return self._container.pop(0)

    def get_container(self):
        """
        Getter for the container used for the queue

        :return: list of midi messages with timestamp
        """
        return self._container

    def clean_unclosed_note_ons(self):
        """
        Removes from the queue the unclosed note_on messages
        """
        for open_note in self._open_note_on_list:
            index = len(self._container) - 1  # the index the we're checking
            # searching for the most recent note_on with note == open_note
            while not (self._container[index]['type'] == 'note_on' and self._container[index]['note'] == open_note):
                index = index - 1
            del self._container[index]  # removing the open note_on message
            self._open_note_on_list.remove(open_note)  # removing the open note reference


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
    result = []  # this list will contain the rhythmical symbols
    for i in range(len(midi_queue)):
        if midi_queue[i]['type'] == 'note_on':
            j = i + 1
            # finding the corresponding subsequent note_off
            while not (midi_queue[j]['type'] == 'note_off' and midi_queue[j]['note'] == midi_queue[i]['note']):
                j = j + 1
            # from here on j is the index of the note_off
            interval = midi_queue[j]['timestamp'] - midi_queue[i]['timestamp']

            # getting the closest rhythmic figure and adding it to the result
            rhythm = get_nearest_rhythm(interval, rhythmical_durations)
            result.append(rhythm)
    return result
