# [Round 17](https://cg.esolangs.gay/17/): check if a number is prime

[*Submitted entry*](https://cg.esolangs.gay/17/#12)

*Relevant files:* `axiom.py`

The `axiom.py` script implements a prime checker function based on the following algorithm:
It is a known result of group theory that finite fields of prime order P have characteristic P.

Unpacking the above, we implement the following:

- For an input N, generate a set S with N unique elements.
- Given N is finite, we can enumerate every possible binary operator S * S -> S.
  - Since there are N * N combinations of input elements, and N possible output elements, there are in total N ^ (N * N) possible such binary operators.
- Pick every pair of such operators, and name them "addition" and "multiplication".
- If the following cases are all satisfied:
  - Addition is associative: for all x, y, z in S, x + (y + z) = (x + y) + z
  - Addition is commutative: for all x, y in S, x + y = y + x
  - Multiplcation is associative: for all x, y, z in S, x * (y * z) = (x * y) * z
  - Multiplcation is commutative: for all x, y in S, x * y = y * x
  - Multiplcation distributes over addition: for all x, y, z in S, x * (y + z) = x * y + x * z
  - Addition has a neutral element: there exists 0 in S such that for all x in S, x + 0 = x
  - Addition has an inverse: for all x in S, there exists some x' in S such that x + x' = 0
  - Multiplication has a neutral element: there exists 1 in S such that for all x in S, x * 1 = x
  - Multiplication has an inverse: for all x in S, there exists some x' in S such that x * x' = 1
  - In the above, 0 is not equal to 1
- Then, S equipped with addition and multiplication forms a finite field, and therefore the following holds:
  - S is of prime order: N = |S| = P^K for some prime P and positive integer K
  - S has a prime characteristic: P = the minimum integer M such that 1 + ... + 1 {M tines} = 0, using the choices for 0 and 1 from above
  - The two values of P above are equal
- Therefore, if from an input N we can form a finite field with characteristic N, we can then conclude that N must be prime.

Very simple and straightforward! How fast does this run? Well, we can do some simple computations to verify the computational complexity with a running tally.
- There are N ^ (N * N) binary operators over a set of size N. We enumerate through them uniformly.
  Tally: O(N ^ (N * N))
- We enumerate through every pair of binary operators. Tally: O(N ^ (N * N) * N ^ (N * N))
- We check the field axioms for each pair of binary operators, which involves a sequence of O(N), O(N^2) and O(N^3) loops, which reduce to O(N^3). We can ignore these because a pithy polynomial term like that means nothing here.
- The total time complexity is... O((N ^ (N ^ 2)) ^ 2), or O((N ^ 2) ^ (N ^ 2)). This is pretty fast for N = 1 or N = 2!

On top of this, the entry makes tasteful use of some wacky python features and DSLs to make for a clean, functional and abstract presentation of the algorithm above.

And there's progress bars. Those are very helpful when trying to run the program for N > 3, to see how many lifetimes of the 
universe it would take to finish running the program.
