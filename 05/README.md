# [Round 5](https://cg.esolangs.gay/5/): Base32-encode a string

[*Submitted entry*](https://cg.esolangs.gay/5/#7)

*Relevant files:* `PYSP.py`

This is one of my favorite entries. I begin by documenting, very poorly and sparsely,
the behavior of a language called "PYSP". It is a "lisplike" language built on top of Python,
with definitions for natural numbers, lists and a brief standard library.

The bulk of the program is setup for the PYSP language, defining its runtime and operations.

The final part is the base32 algorithm itself: It is a single line of code consisting of hundreds of literal
ellipsis objects (`...` in Python), called as functions. This absurd feat is achieved by patching
the ellipsis object in memory using `ctypes` to be callable. This program actually does define an `entry`
function that performs base32 encoding! It took quite a while for me to design and implement this one.

During the guessing phase of this round, PYSP was [introduced to the esolangs wiki](https://esolangs.org/wiki/PYSP).

Fun fact: I initially tried to make this code work using an empty tuple (`()`) instead of an ellipsis (`...`).
Unfortunately, this would segfault my interpreter whenever I tried, so I scrapped that idea.
