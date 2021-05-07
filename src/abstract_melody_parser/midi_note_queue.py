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
        Removes from the queue the unclosed note_on messages.
        """
        for open_note in self._open_note_on_list:
            index = len(self._container) - 1  # the index the we're checking
            # searching for the most recent note_on with note == open_note
            while not (self._container[index]['type'] == 'note_on' and self._container[index]['note'] == open_note):
                index = index - 1
            del self._container[index]  # removing the open note_on message
            self._open_note_on_list.remove(open_note)  # removing the open note reference

    def clear(self):
        """
        Removes all the elements from the queue.
        """
        self._container.clear()
        self._last_timestamp = 0
        self._open_note_on_list = []
