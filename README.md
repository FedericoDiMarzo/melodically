## Introduction

This python module is designed to offer a collection of functions and classes that can be used to give a meaningful interpretation of a succession of midi note messages, in terms of rhythm and melody.

The developement of this project started with the idea of creating a parsing software that could be used to output rhythmic and melodic symbols, that could be further processed by some machine learning algorithm (based on Markov models, grammars or similar techniques).

The output symbols of the parsing are based on the Impro-Visor software notation (https://www.cs.hmc.edu/~keller/jazz/improvisor/) and the theory supporting it can be found at this link https://www.cs.hmc.edu/~keller/jazz/improvisor/papers.html .

## Parsing melodies

The melody parsing allows to translate a midi note number in a abstract melody notation. This parser supports three different abstract melody symbols.

```
c: chord tone
l: color tone
x: random tone
```

An abstract melody can be realized in a particular chord; in order to obtain the correct abstract melody symbol, is necessary to input both a note in standard notation, and a chord. To obtain a note in standard notation from a midi note value, an additional parsing function is needed.

```python
import abstract_melody_parser.melody_parser as mp
note_midi = 48
note_std_notation = mp.parse_midi_note(note_midi)
note_abstract_melody_notation = mp.parse_musical_note(note_std_notation, 'CM')
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
