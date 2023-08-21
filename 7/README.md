# [Round 7](https://cg.esolangs.gay/7/): Decide if a string is valid JSON

[*Submitted entry*](https://cg.esolangs.gay/7/#4)

*Relevant files:* `JSON.py` / `JSON.c` / `JSON.rs` (the same file with 
different extensions for the sake of syntax highlighting), `states.txt`

This round's entry is a 3-language (Python, C, Rust) polyglot that reads in a description
of a context-free grammar's automaton (`states.txt`), compiles it through Python into a LL(1) jump table, 
generates a C program containing said massive (512000 16-bit integers) hard-coded jump table in its source code, and
tests the behavior of it in Rust. All three of these programs are in the same file.

If you can't tell, I am very proud of this entry.

The directory also contains a lot of my brainstorming and auxiliary files for that touch of authenticity.

Enjoy!