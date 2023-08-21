# ignore the hasty and broken code
Entry ← {
    grid ← ⥊¯1↓˘3‿4 ⥊𝕩
    wins ← ⟨
        1‿1‿1‿0‿0‿0‿0‿0‿0 ⋄
        0‿0‿0‿1‿1‿1‿0‿0‿0 ⋄
        0‿0‿0‿0‿0‿0‿1‿1‿1 ⋄
        1‿0‿0‿1‿0‿0‿1‿0‿0 ⋄
        0‿1‿0‿0‿1‿0‿0‿1‿0 ⋄
        0‿0‿1‿0‿0‿1‿0‿0‿1 ⋄
        1‿0‿0‿0‿1‿0‿0‿0‿1 ⋄
        0‿0‿1‿0‿1‿0‿1‿0‿0
    ⟩
    first ← ⊑/'.'=grid
    opts ← first‿⊣
    Get ← ⊑⟜grid∘⊢
    Free ← '.'⊸=∘Get
    picks ← Free ◶opts¨↕9
    Selected ← =∧Free
    Or ← Get˙⊸⋈

    Ending ← {0∨´(⊣≡𝕩⊸∧)¨ wins}
    # tacity into Futures 'x' and Futures 'o'
    futuresX ← <˘picks((Selected)◶(Or 'x')) ⌜↕9
    futuresO ← <˘picks((Selected)◶(Or 'o')) ⌜↕9
    winningX ← Ending¨ 'x'=futuresX
    winningO ← Ending¨ 'o'=futuresO

    Weight ← (2⊸×⊣)+⊢
    values ← winningX Weight¨ winningO
    choice ← 1 ⊑⊑∨ values⋈¨picks
    choice ⊑ futuresX
}
