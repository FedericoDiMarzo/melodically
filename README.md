## Introduction

This python module is designed to offer a collection of functions and classes that can be used to give a meaningful interpretation of a succession of midi note messages, in terms of rhythm and melody.

The developement of this project started with the idea of creating a parsing software that could be used to output rhythmic and melodic symbols, that could be further processed by some machine learning algorithm (based on Markov models, grammars or similar techniques).

The output symbols of the parsing are based on the Impro-Visor software notation (https://www.cs.hmc.edu/~keller/jazz/improvisor/) and the theory supporting it can be found at this link https://www.cs.hmc.edu/~keller/jazz/improvisor/papers.html .

## MidiQueue
To parse note_on/note_off messages, a particular data structure called MidiQueue is used. This queue stores midi note messages with a timestamp, that is needed to parse the rhythmic structure of a melody. This data structure is supposed to collect only melodies, chords are not supported, if multiple note_on messages are pushed into it with timestamps too close with each other, only the first one will be mantained.

In order to insert a new note message with a timestamp included, the get_timestamp_message function must be used.

```python
import abstract_melody_parser as amp

noteQueue = amp.MidiNoteQueue()
noteQueue.push(amp.get_timestamp_msg('note_on', 47))
# some temporal delay...
noteQueue.push(amp.get_timestamp_msg('note_off', 47))
```

Before parsing a midi queue, it's suggested to clean the note_on messages that are still missing the relative note_off message.
```python
noteQueue.clean_unclosed_note_ons()
```

Some other methods are exposed for extra flexibility.
```python
msg = noteQueue.pop() # gets the oldest note message removing it from the queue
list_of_msg = noteQueue.getContainer() # to deal directly with the data container
noteQueue.clear() # clears the queue
```

The use of the MidiQueue for the melodic and rhythic parsing will be explained in the following sections.


## Parsing melodies

The melody parsing allows to translate a midi note number in a abstract melody notation. This parser supports three different abstract melody symbols.

```
c: chord tone
l: color tone
x: random tone
```

An abstract melody can be realized in a particular chord; in order to obtain the correct abstract melody symbol, is necessary to input both a note in standard notation, and a chord. To obtain a note in standard notation from a midi note value, an additional parsing function is needed.

```python

midi_msg = midiQueue.pop()
note_midi = midi_msg['note']
note_std_notation = abs.melody.parse_midi_note(note_midi)
note_abstract_melody_notation = abs.melody.parse_musical_note(note_std_notation, 'CM')
```

The notes in standard notation are uppercase letters, and a sharp symbol can be present (diesis are not used)

```python
musical_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
```

To modify the particular tones (chord or color tones) of a chord or to add a new one, the chord_tones dictionary, inside the chord.py script can be edited.

```python
# excerpt of the dictionary
chord_tones = {
    'CM': {
        'c': ['C', 'E', 'G'], # chord tones can be added here
        'l': ['B', 'D',  'F', 'A'] # color tones can be added here
    },
    # the list continues ...
}
```

## Parsing rhythm

The rhythmic parsing process, allows to translate a series of notes composing a melody, in multiple symbols describing the duration of each note. These are the symbol used to represent the rhythm, they are related to a certain bpm and they refer to a 4/4 rhythmic signature.

```
1: whole note
2: half note
4: quarter note
4dot: quarter note dotted
4t: quarter note triplet
8: eight note
8t: eight note triplet
16: sixteenth note
16t: sixteenth note triplet
```

To define a rhythmic frame for the analysis, a duration dictionary must be created and updated every time the bpm changes.

```python
bpm = 120.5
durations = abs.rhythm.get_durations(bpm)
```
