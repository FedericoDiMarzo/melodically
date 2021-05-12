import time
from melodically.harmony import midi_to_std


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
        self._lastTimestamp = 0

        # list of midi values of the note_on messages that are not closed yet
        self._openNoteOnList = []

        # threshold in seconds to discard notes that are too close
        self._minimumInterval = 0.06

    def push(self, midi_msg):
        """
        Pushes a note_on/off message in the queue.
        If the note_on message is too close with the last note_on, the new entry is discarded.
        If a note_off message doesn't close a note_on message, the new entry is discarded.

        :param midi_msg: dictionary returned by the get_timestamp_msg function
        """

        if midi_msg['type'] == 'note_on':  # note_on case
            # checking if the pushed note_on is too close with the last one
            if midi_msg['timestamp'] - self._lastTimestamp > self._minimumInterval:
                self._lastTimestamp = midi_msg['timestamp']
                self._openNoteOnList.append(midi_msg['note'])
                self._container.append(midi_msg)

        elif midi_msg['type'] == 'note_off':  # note_off case
            # checking if the note_off closes a note on
            if midi_msg['note'] in self._openNoteOnList:
                self._openNoteOnList.remove(midi_msg['note'])
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
        Getter for the container used for the queue.

        :return: list of midi messages with timestamp
        """
        return self._container

    def get_notes(self):
        """
        Gets a list of notes in standard notation from the note on messages.
        :return: list of notes in standard notation
        """
        notes = []
        self.clean_unclosed_note_ons()  # cleaning the container

        for msg in self._container:
            if msg['type'] == 'note_on':
                notes.append(midi_to_std(msg['note']))
        return notes

    def clean_unclosed_note_ons(self):
        """
        Removes from the queue the unclosed note_on messages.
        """
        for open_note in self._openNoteOnList:
            index = len(self._container) - 1  # the index the we're checking
            # searching for the most recent note_on with note == open_note
            while not (self._container[index]['type'] == 'note_on' and self._container[index]['note'] == open_note):
                index = index - 1
            del self._container[index]  # removing the open note_on message
        self._openNoteOnList.clear()  # removing the open note references

    def clear(self):
        """
        Removes all the elements from the queue.
        """
        self._container.clear()
        self._lastTimestamp = 0
        self._openNoteOnList = []


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
