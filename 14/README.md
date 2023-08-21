# [Round 14](https://cg.esolangs.gay/14/): Perform a dot product

[*Submitted entry*](https://cg.esolangs.gay/14/#)

*Relevant files:* `file.py`

This is one of my masterpieces. This whole file is in 39 columns, full to the brim
with details, including code review, inline advertisements and even a brief conversation
about the universe. There is also the binary data associated with a doctored low-resolution
screenshot of sans undertale, annotated with "SANS!" and "Olivia". It was pretty blatant.

Moreover, this code was made in conspiracy with IFColtransG to create a collaborative entry:
- When the program is run normally, it fetches the cg.esolangs.gay/14 website and downloads each entry.
- It fetches each program that is not my entry.
- It tries to execute each entry as a python script, with the `-x` command line parameter.
  This parameter, typically used for non-unix script shebangs, skips the first line of code for execution.
  IFColtransG and I conspired such that our program has different behavior when executed with and without
  the first line of code. (Their entry is #4, and performs the same thing when run normally.)
- The foreign program asks for input. We also conspired on the format of data transfer:
  The programs communicate using [MESON](https://esolangs.org/wiki/MESON) over STDIN/STDOUT. 
  The source sends a 2-tuple of lists of integers, and expects to receive an integer in return, 
  representing the dot product of those two lists.
- My "hidden" program solves the task inductively, that is, it performs a dot product by 
  first multiplying one pair of numbers and then outsourcing the rest of the solution to another entry
  as if running normally. (Unfortunately, we didn't both do this tactic. If we did, the result would be
  that we traded back and forth solving parts of a single dot product.)
- As a fun bonus, the "doc comment" at the start of the program is actually not a comment at all when
  running in `-x` mode. This means that all of its lines are executed as standard python, including
  `input or output (undefined. seriously,)`, `0>0>_<0<_[RAID:SHADOW-LEGENDS]>>0>_<0<0`, and
  `(... for tuning in today (it is kind,))`. These all abuse Python's short circuiting and lazy evaluation
  facilities to create code that looks impossible.

