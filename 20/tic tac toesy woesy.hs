import Data.List as L
import Control.Monad.Identity as I

main = pure ㅤ

-- blame me for: motation 
ㅤ :: ()
ㅤ = ()
infixr 0 ⠀
(⠀) :: () -> a -> I.Identity a
ㅤ⠀x = return x
infixr 0 ⠀⠀
(⠀⠀) :: () -> I.Identity a -> a
ㅤ⠀⠀x = I.runIdentity x
infixr 7 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
(⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀) :: (b -> c -> d) -> (a -> c) -> a -> b -> d
g⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀h = \w x -> g x (h w) 
infixr 7 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
(⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀) :: () -> (a -> a -> c) -> a -> c
ㅤ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀g = \x -> x `g` x
infixr 7 ⠀⠀⠀⠀
(⠀⠀⠀⠀) :: (a -> b) -> (a -> b -> d) -> a -> d
f⠀⠀⠀⠀g = \x -> g x (f x)
infixr 7 ⠀⠀⠀⠀⠀
(⠀⠀⠀⠀⠀) :: (c -> d -> e) -> (a -> b -> d) -> a -> b -> c -> e
g⠀⠀⠀⠀⠀h = \w x y -> g y (h w x)
infixr 7 ⠀⠀⠀⠀⠀⠀
(⠀⠀⠀⠀⠀⠀) :: (a -> b -> c) -> (a -> b -> c -> e) -> a -> b -> e
f⠀⠀⠀⠀⠀⠀g = \w x -> g w x (f w x)
infixr 7 ⠀⠀⠀⠀⠀⠀⠀
(⠀⠀⠀⠀⠀⠀⠀) :: (b -> c) -> (a -> b) -> a -> c
f⠀⠀⠀⠀⠀⠀⠀g = f . g
infixr 7 ⠀⠀⠀⠀⠀⠀⠀⠀
(⠀⠀⠀⠀⠀⠀⠀⠀) :: (c -> d) -> (a -> b -> c) -> a -> b -> d
f⠀⠀⠀⠀⠀⠀⠀⠀g = \w x -> f (g w x)
infixl 1 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
(⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀) :: (a -> b) -> a -> b
f⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀x = f x
infixl 9 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ -- for fake infix
(⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀) :: a -> b -> (a, b)
(⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀)=(,)
infixr 8 ⠀⠀⠀
(⠀⠀⠀) :: a -> () -> [a]
x⠀⠀⠀ㅤ = [x]
infixr 8 ‿
(‿) :: a -> [a] -> [a]
w‿x = w:x
infixr 9 ¯
(¯) :: () -> Int -> Int
ㅤ¯i = 0 - i
infixr 2 ＜ -- ⟨invalid⟩
(＜) :: () -> [a] -> [a]
ㅤ＜x = x
infixr 2 ＞
(＞) :: a -> () -> [a]
x＞ㅤ=[x]
infixr 2 ⋄
(⋄) :: a -> [a] -> [a]
(⋄) = (‿)
infixl 8 ∘
(∘) :: (b -> c) -> (a -> b) -> a -> c
f ∘ g = \x -> f (g x)
infixl 5 ∘⠀
(∘⠀) :: (c -> d) -> (a -> b -> c) -> a -> b -> d
f ∘⠀g = \w x -> f (g w x)
infixl 5 ˜
(˜ ) :: (a -> a -> b) -> () -> (a -> b)
f ˜ㅤ = \x -> f x x 
infixl 5 ˜⠀
(˜⠀) :: (a -> b -> c) -> () -> (b -> a -> c)
f ˜⠀ㅤ= \w x -> f x w
infixl 5 ˙
(˙ ) :: a -> () -> (b -> a)
f ˙ㅤ = \x -> f
infixl 5 ˙⠀
(˙⠀) :: a -> () -> (b -> c -> a)
f ˙⠀ㅤ= \w x -> f
infixl 5 ○
(○ ) :: (b -> c) -> (a -> b) -> a -> c
f ○ g = \x -> f (g x)
infixl 5 ○⠀
(○⠀) :: (b -> b -> c) -> (a -> b) -> a -> a -> c
f ○⠀g = \w x -> f (g w) (g x)
infixl 5 ⊸
(⊸ ) :: b -> (b -> a -> c) -> a -> c
f ⊸ g = g f
infixl 5 ⊸⠀
(⊸⠀) :: (a -> b) -> (b -> c -> d) -> a -> c -> d
f ⊸⠀g = \w x -> g (f w) x
infixl 5 ⟜
(⟜ ) :: (a -> b -> c) -> b -> a -> c
f ⟜ g = \x -> f x g
infixl 5 ⟜⠀
(⟜⠀) :: (a -> c -> d) -> (b -> c) -> a -> b -> d
f ⟜⠀g = \w x -> f w (g x)
infixl 5 ◶
(◶) :: (a -> Int) -> [a -> b] -> a -> b
f ◶ g = \x -> (g !! f x) x
infixl 5 ◶⠀
(◶⠀) :: (a -> b -> Int) -> [a -> b -> c] -> a -> b -> c
f ◶⠀g = \w x -> (g !! f w x) w x
infixl 5 ˘
(˘) :: (a -> b -> c) -> () -> a -> [b] -> [c]
f˘ㅤ = fmap . f
infixl 5 ¨
(¨) :: (a -> b) -> () -> [a] -> [b]
f¨ㅤ = fmap f
infixl 5 ´
(´) :: (a -> b -> b) -> () -> b -> [a] -> b
f´ㅤ = foldr f
infixl 5 ⌜
(⌜) :: ([a], (a -> b -> c)) -> () -> [b] -> [[c]]
(ws,f)⌜ㅤ= \xs -> [[f w x | x <- xs] | w <- ws]
infixl 5 ¨⠀⠀
(¨⠀⠀) :: ([a], (a -> b -> c)) -> [b] -> [c] -- inconsistent
(ws,f)¨⠀⠀xs = uncurry (f) <$> zip ws xs
infixr 3 ⥊
(⥊) :: [Int] -> [a] -> [[a]]
[a,b]⥊x = take b <$> (take a $ iterate (drop b) (x++x)) -- fill
_⥊x = undefined
infixr 3 ⠀⥊
(⠀⥊) :: () -> [[a]] -> [a]
ㅤ⠀⥊x = L.concat x
infixr 3 ↓
(↓) :: Int -> [a] -> [a]
w↓x = let op = case compare w 0 of 
            LT -> reverse . drop (0-w) . reverse
            EQ -> id
            GT -> drop w
        in 
            op x
infixr 3 ＝
(＝) :: Eq a => a -> [a] -> [Int]
w＝x = fromEnum . (==) w <$> x
infixr 3 ⠀＝
(⠀＝) :: Eq a => a -> a -> Int
w⠀＝x = fromEnum (w == x)
infixr 3 ／
(／) :: () -> [Int] -> [Int] 
ㅤ／x = elemIndices 1 x -- boolean
infixr 3 ⊑
(⊑) :: () -> [a] -> a
ㅤ⊑x = head x
infixr 3 ⠀⊑
(⠀⊑) :: Int -> [a] -> a -- vector
w⠀⊑x = x !! w
infixr 3 ↕
(↕) :: () -> Int -> [Int]
ㅤ↕x = [0..x-1]
infixr 3 ⊣ -- arity hack
(⊣) :: a -> a
(⊣) = id
infixr 3 ⊢
(⊢) :: a -> b -> b
(⊢) = const id
infixr 3 ∧
(∧) :: Int -> Int -> Int
w∧x = fromEnum $ w/=0 && x/=0
infixr 3 ⋈
(⋈) :: a -> a -> [a]
x⋈y = [x,y]
infixr 3 ∨
(∨) :: Int -> Int -> Int
w∨x = fromEnum $ w/=0 || x/=0
infixr 3 ≡
(≡) :: [Int] -> [Int] -> Int
[]≡[] = 1
w:ws≡x:xs = (fromEnum $ w == x) * (ws≡xs)
_≡_=undefined
infixr 3 ﹤ -- fake
(﹤) :: () -> a -> a
ㅤ﹤x=x
infixr 3 ﹦ -- specialize
(﹦) :: Eq a => a -> [[a]] -> [[Int]]
w﹦xss = fmap (fromEnum . (==) w) <$> xss
infixr 3 ×
(×) :: Int -> Int -> Int
(×) = (*)
infixr 3 ＋ -- unshadow
(＋) :: Int -> Int -> Int
(＋) = (+)
infixr 3 ⊣⠀ -- yay
(⊣⠀) :: a -> b -> a
w⊣⠀_=w
infixr 3 ∨⠀
(∨⠀) :: Ord a => () -> [a] -> [a]
ㅤ∨⠀x = reverse $ sort x

-- blame haskell for: bad motation
infixr 3 ‿⊣
(‿⊣) :: a -> () -> [(a -> a)] -- scalar autoconst w
w‿⊣ㅤ = (const w)‿(⊣)⠀⠀⠀ㅤ
infixr 3 ↓˘ 
(↓˘) :: Int -> [[a]] -> [[a]]
w↓˘x = ((↓)˘ㅤ) w x
infixl 4 ⊑⟜
(⊑⟜) :: () -> [a] -> Int -> a
ㅤ⊑⟜g = (⠀⊑)⟜g
infixr 3 ⊸＝∘
(⊸＝∘) :: Eq a => a -> (b -> b -> a) -> b -> b -> Int -- clean
w⊸＝∘x = (w⊸(⠀＝))∘⠀x
infixr 3 ¨⠀
(¨⠀) :: (a -> b) -> [a] -> [b]
(¨⠀) = fmap
infixl 4 ∘⊢
(∘⊢) :: (b -> c) -> () -> a -> b -> c
f∘⊢ㅤ = f∘⠀(⊢)
infixl 4 ˙⊸⋈
(˙⊸⋈) :: (a -> a -> b) -> () -> b -> [a -> a -> b]
f˙⊸⋈ㅤ = \x -> (f⊸(⋈)) (const.const x) -- autoconst v2
infixr 3 ∨´
(∨´) :: Int -> [Int] -> Int
w∨´x = ((∨)´ㅤ) w x
infixr 3 ⊸∧
(⊸∧) :: [Int] -> () -> [Int] -> [Int]
w⊸∧ㅤ = \x -> uncurry (∧) <$> zip w x
infixr 3 ⊣≡
(⊣≡) :: () -> ([Int] -> [Int]) -> [Int] -> Int
ㅤ⊣≡f = \x -> ((⊣)x)≡(f x)
infixr 3 ﹤˘ -- fake because flat
(﹤˘) :: () -> a -> a
ㅤ﹤˘x=x
infixr 3 ⌜↕ -- cheater
(⌜↕) :: ([a], (a -> Int -> c)) -> Int -> [[c]]
(w,f)⌜↕x = ((w,f)⌜ㅤ)(ㅤ↕x)
infixr 3 ⊸×⊣ -- no train
(⊸×⊣) :: Int -> () -> Int -> Int -> Int
w⊸×⊣ㅤ = (w⊸(×))∘⠀(⊣⠀)
infixr 3 ⋈¨
(⋈¨) :: [a] -> [a] -> [[a]]
w⋈¨x = w ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀(⋈)¨⠀⠀ x -- zoop


{------------------------------------------------
 - PROGRAM STARTS HERE                          -
 -                                              -
 -                                              -
 -                                              -
 -----------------------------------------------}

entry    :: [Char] ->    [Char]
entry = (\𝕩 ->ㅤ⠀⠀(do -- {
        grid <-ㅤ⠀ㅤ⠀⥊ㅤ¯1↓˘3‿4⠀⠀⠀ㅤ⥊𝕩
        wins <-ㅤ⠀(
            ㅤ＜               
                1‿1‿1‿0‿0‿0‿0‿0‿0⠀⠀⠀ㅤ ⋄
                0‿0‿0‿1‿1‿1‿0‿0‿0⠀⠀⠀ㅤ ⋄
                0‿0‿0‿0‿0‿0‿1‿1‿1⠀⠀⠀ㅤ ⋄
                1‿0‿0‿1‿0‿0‿1‿0‿0⠀⠀⠀ㅤ ⋄
                0‿1‿0‿0‿1‿0‿0‿1‿0⠀⠀⠀ㅤ ⋄
                0‿0‿1‿0‿0‿1‿0‿0‿1⠀⠀⠀ㅤ ⋄
                1‿0‿0‿0‿1‿0‿0‿0‿1⠀⠀⠀ㅤ ⋄
                0‿0‿1‿0‿1‿0‿1‿0‿0⠀⠀⠀ㅤ
            ＞ㅤ
            )
        
        first <-ㅤ⠀ㅤ⊑ㅤ／'.'＝grid
        opts <-ㅤ⠀first‿⊣ㅤ
        ㅤGet <-ㅤ⠀ㅤ⊑⟜grid∘⊢ㅤ
        ㅤFree <-ㅤ⠀'.'⊸＝∘ㅤGet
        picks <-ㅤ⠀ㅤ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ㅤFree◶opts¨ㅤ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ㅤ↕9
        ㅤSelected <-ㅤ⠀(⠀＝)⠀⠀⠀⠀⠀⠀(∧)⠀⠀⠀⠀⠀ ㅤFree
        ㅤOr <-ㅤ⠀ㅤGet˙⊸⋈ㅤ
        
        ㅤEnding <-ㅤ⠀ (\𝕩 -> -- {
            (0∨´(ㅤ⊣≡𝕩⊸∧ㅤ)¨⠀wins)
            ) -- }
        -- tacify into Futures 'x' and Winning 'x'
        futuresX <-ㅤ⠀ㅤ﹤˘picks⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀((ㅤSelected)◶⠀(ㅤOr 'x'))⌜↕9
        futuresO <-ㅤ⠀ㅤ﹤˘picks⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀((ㅤSelected)◶⠀(ㅤOr 'o'))⌜↕9
        winningX <-ㅤ⠀ㅤEnding¨⠀'x'﹦futuresX
        winningO <-ㅤ⠀ㅤEnding¨⠀'o'﹦futuresO

        ㅤWeight <-ㅤ⠀(2⊸×⊣ㅤ)⠀⠀⠀⠀⠀⠀(+)⠀⠀⠀⠀⠀(⊢)
        values <-ㅤ⠀winningX⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ㅤWeight¨⠀⠀ winningO
        choice <-ㅤ⠀1⠀⊑ㅤ⊑ㅤ∨⠀values⋈¨picks
        ㅤ⠀choice ⠀⊑ futuresX
    )) -- }

(⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠛⠉⠉⠉⠉⠉⠉⠛⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠛⠉⠉⠉⠉⠉⠉⠛⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠛⠉⠉⠉⠉⠉⠉⠛⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿)=ㅤ
(⣿⣿⣿⣿⣿⣿⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⣿⣿⣿⣿⣿⣿)=ㅤ
(⣿⣿⣿⣿⣿⣿⡇⠀⢀⣀⣀⣀⠀⠀⠀⠀⣀⣀⣀⡀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⢀⣀⣀⣀⠀⠀⠀⠀⣀⣀⣀⡀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⢀⣀⣀⣀⠀⠀⠀⠀⣀⣀⣀⡀⠀⢸⣿⣿⣿⣿⣿⣿)=ㅤ
(⣿⣿⣿⣿⣿⣿⡇⢰⣿⣿⠛⣿⡇⠀⠀⢸⣿⠛⣿⣿⡆⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢰⣿⣿⠛⣿⡇⠀⠀⢸⣿⠛⣿⣿⡆⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢰⣿⣿⠛⣿⡇⠀⠀⢸⣿⠛⣿⣿⡆⢸⣿⣿⣿⣿⣿⣿)=ㅤ
(⣿⣿⣿⣿⣿⣿⣷⠄⠉⠛⣛⠟⠀⣼⣧⠀⠻⣛⠛⠉⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠄⠉⠛⣛⠟⠀⣼⣧⠀⠻⣛⠛⠉⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠄⠉⠛⣛⠟⠀⣼⣧⠀⠻⣛⠛⠉⠀⣾⣿⣿⣿⣿⣿⣿)=ㅤ
(⣿⣿⣿⣿⣿⣿⣿⠀⠤⡖⡤⣀⣀⣉⣉⣀⣀⡠⣴⠦⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠤⡖⡤⣀⣀⣉⣉⣀⣀⡠⣴⠦⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠤⡖⡤⣀⣀⣉⣉⣀⣀⡠⣴⠦⠀⣿⣿⣿⣿⣿⣿⣿)=ㅤ
(⣿⣿⣿⣿⡿⠛⢻⣆⠀⠈⠃⠤⡇⢸⠀⢸⠠⠗⠉⠀⣠⠟⠉⢻⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⢻⣆⠀⠈⠃⠤⡇⢸⠀⢸⠠⠗⠉⠀⣠⠟⠉⢻⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⢻⣆⠀⠈⠃⠤⡇⢸⠀⢸⠠⠗⠉⠀⣠⠟⠉⢻⣿⣿⣿⣿)=ㅤ
(⣿⣿⣿⣿⣴⣦⣤⡉⠳⣶⣦⣤⣄⣤⣤⣤⣤⣴⣶⡾⠁⣠⣾⣯⠻⣿⣿⣿⣿⣿⣿⣿⣴⣦⣤⡉⠳⣶⣦⣤⣄⣤⣤⣤⣤⣴⣶⡾⠁⣠⣾⣯⠻⣿⣿⣿⣿⣿⣿⣿⣴⣦⣤⡉⠳⣶⣦⣤⣄⣤⣤⣤⣤⣴⣶⡾⠁⣠⣾⣯⠻⣿⣿⣿)=ㅤ
(⣿⣿⢟⣽⣿⡟⢻⣿⣶⡌⣙⠛⣄⠉⠁⡼⠛⢛⣡⣤⣾⡟⢹⣿⣷⡜⢿⣿⣿⣿⢟⣽⣿⡟⢻⣿⣶⡌⣙⠛⣄⠉⠁⡼⠛⢛⣡⣤⣾⡟⢹⣿⣷⡜⢿⣿⣿⣿⢟⣽⣿⡟⢻⣿⣶⡌⣙⠛⣄⠉⠁⡼⠛⢛⣡⣤⣾⡟⢹⣿⣷⡜⢿⣿)=ㅤ
(⣿⢣⣿⣿⣿⡇⠸⡿⠿⠃⣋⢸⡏⠉⠙⡟⢈⢸⣿⡿⠟⡁⢸⣿⣿⣿⡆⢻⣿⢣⣿⣿⣿⡇⠸⡿⠿⠃⣋⢸⡏⠉⠙⡟⢈⢸⣿⡿⠟⡁⢸⣿⣿⣿⡆⢻⣿⢣⣿⣿⣿⡇⠸⡿⠿⠃⣋⢸⡏⠉⠙⡟⢈⢸⣿⡿⠟⡁⢸⣿⣿⣿⡆⢻)=ㅤ
(⣇⠸⣿⣿⣿⠃⣴⣾⣿⣿⢘⡅⡇⠀⠀⡇⣭⢸⢱⣶⣿⣧⠈⣿⣿⣿⣿⢸⣇⠸⣿⣿⣿⠃⣴⣾⣿⣿⢘⡅⡇⠀⠀⡇⣭⢸⢱⣶⣿⣧⠈⣿⣿⣿⣿⢸⣇⠸⣿⣿⣿⠃⣴⣾⣿⣿⢘⡅⡇⠀⠀⡇⣭⢸⢱⣶⣿⣧⠈⣿⣿⣿⣿⢸)=ㅤ
(⣿⣷⣌⠛⢿⠀⣿⣿⣿⣿⡎⡄⣇⣀⣀⡇⡆⢣⣿⣿⣿⣿⠀⣿⣿⠟⣡⣾⣿⣷⣌⠛⢿⠀⣿⣿⣿⣿⡎⡄⣇⣀⣀⡇⡆⢣⣿⣿⣿⣿⠀⣿⣿⠟⣡⣾⣿⣷⣌⠛⢿⠀⣿⣿⣿⣿⡎⡄⣇⣀⣀⡇⡆⢣⣿⣿⣿⣿⠀⣿⣿⠟⣡⣾)=ㅤ
(⣿⣿⣿⣷⣾⣄⣈⣛⣛⣛⣣⣤⣤⣶⣶⣶⣤⣭⣭⣭⣭⣁⣰⣥⣴⣿⣿⣿⣿⣿⣿⣷⣾⣄⣈⣛⣛⣛⣣⣤⣤⣶⣶⣶⣤⣭⣭⣭⣭⣁⣰⣥⣴⣿⣿⣿⣿⣿⣿⣷⣾⣄⣈⣛⣛⣛⣣⣤⣤⣶⣶⣶⣤⣭⣭⣭⣭⣁⣰⣥⣴⣿⣿⣿)=ㅤ
(⣿⣿⣿⣿⣿⣿⢟⣿⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⠉⣿⣿⣏⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢟⣿⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⠉⣿⣿⣏⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢟⣿⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⠉⣿⣿⣏⢿⣿⣿⣿⣿⣿)=ㅤ
(⣿⣿⣿⣿⣿⣿⢸⡇⢀⣿⣿⣿⣿⠉⡎⣿⣿⣿⠀⢻⣿⣿⡸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⡇⢀⣿⣿⣿⣿⠉⡎⣿⣿⣿⠀⢻⣿⣿⡸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⡇⢀⣿⣿⣿⣿⠉⡎⣿⣿⣿⠀⢻⣿⣿⡸⣿⣿⣿⣿⣿)=ㅤ
(⣿⣿⣿⣿⣿⡇⣿⠁⣾⣿⣿⣿⣿⣠⣿⢹⣿⣿⡄⢸⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⠁⣾⣿⣿⣿⣿⣠⣿⢹⣿⣿⡄⢸⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⠁⣾⣿⣿⣿⣿⣠⣿⢹⣿⣿⡄⢸⣿⣿⡇⣿⣿⣿⣿⣿)=ㅤ
(⣿⣿⣿⣿⣿⣇⣉⣀⠻⠿⠿⠿⠟⣿⣿⡸⠿⠿⠇⠈⠿⣋⣁⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⣉⣀⠻⠿⠿⠿⠟⣿⣿⡸⠿⠿⠇⠈⠿⣋⣁⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⣉⣀⠻⠿⠿⠿⠟⣿⣿⡸⠿⠿⠇⠈⠿⣋⣁⣿⣿⣿⣿⣿)=ㅤ
(⣿⣿⣿⣿⡿⠛⠛⠿⣛⠛⢿⣿⣿⣿⣿⣿⣿⠋⠛⠛⢛⡿⠟⠛⠿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠛⠿⣛⠛⢿⣿⣿⣿⣿⣿⣿⠋⠛⠛⢛⡿⠟⠛⠿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠛⠿⣛⠛⢿⣿⣿⣿⣿⣿⣿⠋⠛⠛⢛⡿⠟⠛⠿⣿⣿⣿)=ㅤ
(⣿⣿⣿⣿⣀⣀⣀⣀⣀⣖⣻⣿⣿⣿⣿⣿⣟⣒⣒⣲⣁⣀⣀⣀⣀⣼⣿⣿⣿⣿⣿⣿⣀⣀⣀⣀⣀⣖⣻⣿⣿⣿⣿⣿⣟⣒⣒⣲⣁⣀⣀⣀⣀⣼⣿⣿⣿⣿⣿⣿⣀⣀⣀⣀⣀⣖⣻⣿⣿⣿⣿⣿⣟⣒⣒⣲⣁⣀⣀⣀⣀⣼⣿⣿)=ㅤ
ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤsansㅤundertale                                                                 =ㅤ

{------------------------------------------------
 - PROGRAM ENDS HERE                            -
 -                                              -
 -                                              -
 -                                              -
 -----------------------------------------------}