⍝ where π is a function returning every permutation of an array
entry ← {⊃ ⍵{∧/⍵∊¨⍺} ⌽ π∘⍳ ≢⍵}
⎕←(⊢entry (1 2 3) (,2) (2 3))