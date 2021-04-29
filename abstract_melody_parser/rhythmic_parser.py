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
    A midi queue containing note_on/off midi messages and timestamps.
    This queue is used by the rhythmic parser algorithm.
    """

    def __init__(self):
        # container used to implement the queue
        self._container = []

        # timestamp of the last note_on message
        self._last_timestamp = 0

        # midi value of the last note_on message
        self._last_note_on_value = -1

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
                self._last_note_on_value = midi_msg['note']
                self._container.append(midi_msg)

        elif midi_msg['type'] == 'note_off':  # note_off case
            # checking if the note_off closes a note on
            if midi_msg['note'] == self._last_note_on_value:
                self._container.append(midi_msg)

        # all other types of midi messages are excluded automatically

    def pop(self):
        """
        Pops a midi message from the queue.

        :return: midi message
        """
        return self._container.pop()
