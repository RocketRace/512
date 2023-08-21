# [Round 32](https://cg.esolangs.gay/32/): Generate a maze

[*Submitted entry*](https://cg.esolangs.gay/32/#7)

*Relevant files:* `maze.zc`

Conway's game of life can form surprisingly maze-like structures. In fact, using the B3/S12345 (known as the "Maze ruleset"),
the equilibrium state for a grid has mazelike structure! Therefore, this entry implements Life (as well as all other elementary
lifelike cellular automata)!

The code is written in Zirconium, one of my own esolangs. It forms a very elaborate network of drone stations, timed
just so that the console output is a random maze consisting of "#" and " " characters. As seen in the header macros,
you can also configure the program to alter the rule of the life-like simulation used, the number of steps of 
evaluation, and the symbols used in the output.
