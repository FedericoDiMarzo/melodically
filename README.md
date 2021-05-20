## Introduction

This python module is designed to offer a collection of functions, classes and data structures that can be used to represent notes, rhythmic figures and melodies. Various parser are available to give a meaningful interpretation of a succession of midi note messages, together with a tool to monitor the evolution of an harmonic state of a musical performance.

The developement of this project started with the main idea of offering a series of useful tools that can be used to track external midi note messages that form melodies, generating sequences and harmonic information, that could be further processed by some machine learning algorithm (based on Markov models, grammars or similar techniques).

The output symbols of the parsing are based on the Impro-Visor software notation (https://www.cs.hmc.edu/~keller/jazz/improvisor/) and the theory supporting it can be found at this link https://www.cs.hmc.edu/~keller/jazz/improvisor/papers.html .

## Installation
The package can easily be installed using the pip package manager.
```shell
pip install melodically
```

## MidiNoteQueue
To parse note_on/note_off messages, a particular data structure called MidiQueue is used. This queue stores midi note messages with a timestamp, that is needed to parse the rhythmic structure of a melody. This data structure is supposed to collect only melodies, chords are not supported, if multiple note_on messages are pushed into it with timestamps too close with each other, only the first one will be mantained.

```python
import melodically as m

note_queue = m.MidiNoteQueue()
note_queue.push(msg_type='note_on', note=47)
# some temporal delay...
note_queue.push(msg_type='note_off', note=47)
```

Some other methods are exposed for extra flexibility.

```python
msg = note_queue.pop() # gets the oldest note message removing it from the queue
list_of_msg = note_queue.get_container() # to deal directly with the data container
musical_notes = note_queue.get_notes() # to obtain a list of notes in std notation
note_queue.clean_unclosed_note_ons() # removes note_on messages that don't have a corrisponding note_off
note_queue.clear() # clears the queue
```

The use of the MidiQueue for the melodic and rhythic parsing will be explained in the following sections.

## HarmonicState
The HarmonicState class allows to track the harmonic relations of an input melody notes. 

```python
harmonic_state = m.HarmonicState(buffer_size=20)
```

The internal buffer is used to store input notes, in order to analyze them when it will be needed.

```python
doric_melody = ['C#', 'C#', 'D#', 'E', 'F#', 'G#', 'A#', 'B']
harmonic_state.push_notes(doric_melody)
```

The HarmonicState can be sampled, to return the notes of the closest modal scale, depending on the notes in the input buffer. 

```python
current_scale = harmonic_state.get_mode_notes()
```

In order to compute the most affine scale, the notes in the input buffer are compared with a distance function to each possible sequence of notes that composes a modal scale. The modal scale that minimizes this distance is then chosen. 

The state update can also be forced manually if needed.

```python
harmonic_state.update_scale()
```

## Parsing single notes

The note parsing allows to translate a midi note number in a abstract melody notation. This parser supports three different abstract melody symbols.

```
c: chord tone
l: color tone
x: random tone
```

An abstract melody can be realized in a particular chord; in order to obtain the correct abstract melody symbol, is necessary to input both a note in standard notation, and a chord. To obtain a note in standard notation from a midi note value, an additional parsing function is needed.

```python
note = 'G'
chord = 'CM' # C major chord
abstract_note = m.parse_musical_note(note, chord) # from std note notation to abstract note notation
```

The notes in standard notation are uppercase letters, and a sharp symbol can be present (an alternative version with flats is also present).

```python
musical_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
musical_notes_b = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
```

The chord_dict dictionary contains the lists of chord/color tones of each chord.
At the moment only few families of chords are supported

```
# chord notation
CM: major
Cm: minor
C7: dominant
```

Example on how to extract the lists of chord/color tones

```python
# chord and color tones for the chord C7
chord_tones = chord_dictionary['C7']['c']
color_tones = chord_dictionary['C7']['l']
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

the rests are indicated with an "r" prefix
ex: r4 (quarter note rest)
```

To define a rhythmic frame for the analysis, a duration dictionary must be created and updated every time the bpm changes.

```python
bpm = 120.5
durations = amp.get_durations(bpm)
```

After defining the durations from the bpm, the parsing can follow. It will return a list of symbols for all the notes in the melody.

```python
rhythmic_symbols = amp.parse_rhythm(note_queue, durations)
```

## Manage rhythmic sequencrs into measures

Given any rhythmical sequence, the user can verify if it fits inside the '4/4' rhythmical subdivision.

```python
rhythmic_sequence = [...]
measures = 2

# example
if sequence_fit_measures(rhythmic_sequence, measures)
  print("The sequence fits into given measure")

```

Alternatively, given a specific number of measures, the following method will return a new list of rhythmical symbols that can fit into it.

```python
rhythmic_sequence = [...]
measures = 3

symbols = clip_rhythmic_sequence(rhythmic_sequence, measures)

# example
symbols = [...]

```

## Parsing entire melodies

Sometimes the informative content of a melody can only be found in the rhythm or in the armonic relations between the notes and a chord, but in many other occasions, is the underlying relation between the two that really expresses the message that a musitian is trying to share with his/her performance. Following this perspective, it can be useful to perform both melodic and rhythmic parsing from a single MidiQueue, and read the resulting symbols as pairs. Let's suppose to parse a MidiQueue that contains a melody playing on a Dm chord

```python
current_chord = 'Dm'
bpm = 125
durations = m.get_durations(bpm)
full_melody = m.parse_melody(midi_queue, current_chord, durations)
```

The output symbols of a melodic parsing, are just a combination of the abstract note symbols and the rhythmic symbols.

``` python
# example melody
['c4', 'c4', 'x8', 'x8', 'r4', 'l2', 'r2', 'l1']

```

## Enriching a chord dictionary

Dealing with the autogeneration of chords or melodies, the user easily realizes the importance to enrich his dictionary with color chords (chords composed by four notes withspecificintervals). From this concept, we develop a method that returns all the musical connections that a single chord can provide.

The user can add all the Major, Minor, or Dominant 7th to a given chord dictionary.

```python
chord_dict = [...]
upd_chord_dict = m.get_chord_tones(chord_dict)

# example of a new dictionary
upd_chord_dict = [...]
```


## Handling with MIDI protocol


Often, dealing with the MIDI protocol, would be beneficial to have a method that automatically gives all MIDI values of all the notes that compose a single chord.

An octave parameter can be specified as a integer indicating the octave shared between the notes, as a list of integers, indicating the octave for each note of the chords (in this case, the size of the list must be the same of the number of chord tones of the chord).

```python
chord = 'Am'
midi_chord = m.chord_to_midi(chord, octave=3)

# example for the given chord
midi_chord = [...]
```


