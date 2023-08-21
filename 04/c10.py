import re, inspect, sys
# f . f     f @ x      x >> f
class __Compose:
	def __init__(self, *__fs):
		self.__fs = __fs

	def __getattr__(self, __f):
		return type(self)(*self.__fs, eval(__f, globals(), inspect.currentframe().f_back.f_locals))
	
	def __matmul__(self, __x):
		return self(__x)

	__rrshift__ = __matmul__

	def __call__(self, *__xs):
		__fs = list(self.__fs)
		__x = __fs.pop()(*__xs)
		while len(__fs) != 0:
			__x = __fs.pop()(__x)
		return __x
# Macron
def __macro(__code):
	for _ in range(1000):
		__code = re.sub(r"\(([^\(]*?)\) -> (.*)", r"__Compose(lambda \1: \2)", __code)
	return __code
# Do
def __runner(__code):
	sys.setrecursionlimit(100000)
	exec(__macro(__code), globals())
# Codes
__runner("""
id = (x) -> x
part = (f, *xs) -> (x) -> f (*xs, x)
use0 = (f) -> (*xs) -> f ()
wuse0 = (x) -> (*xs) -> x
use1 = (f) -> (x, *xs) -> f (x)

nuple = (*xs) -> xs
dewrapply = (f, xs) -> f(*xs)

nil = () -> []
cons = (x, xs) -> [x] + xs
head = (xs) -> xs[0]
tail = (xs) -> xs[1:]

n = (xs) -> len (xs)
consnil = (x) -> cons (x, nil ())

eq = (x, y) -> x == y
z = () -> 0
s = (x) -> x + 1
thirtytwo = () -> 32
pre = (x) -> sub (x, s . z ())
eqz = (xs) -> eq (z (), xs)
eqzn = (xs) -> eqz . n @ xs
eq1 = (xs) -> eq (s . z (), xs)
eq1n = (xs) -> eq1 . n @ xs

capply = (cf, tf, ff) -> (*xs) -> tf (*xs) if cf (*xs) else ff (*xs)
fdeconsapply = (f, hf, tf, xs) -> f (hf . head @ xs, tf . tail @ xs)
consapply = (hf, tf, xs) -> fdeconsapply (cons, hf, tf, xs)

fold = (f, xs) -> xs >> capply (eq1n, head, part (fdeconsapply, f, id, part (fold, f))) 
applyn = (f, xs) -> xs >> capply (eq1n, consnil . f . head, part (consapply, f, part (applyn, f)))
headapplyn = (f, xs) -> applyn (part (f, head @ xs), tail @ xs)

ziphead2 = (xs, ys) -> nuple (head @ xs, head @ ys)
tails2 = (xs, ys) -> nuple (tail @ xs, tail @ ys)
zip2tails = (xs, ys) -> dewrapply (zip2, tails2 (xs, ys))
zip2 = (xs, ys) -> cons (ziphead2 (xs, ys), capply (use1 @ eq1n, use0 @ nil, zip2tails) (xs, ys))

add = (x, y) -> x + y
vadd = (xs, ys) -> applyn (part (dewrapply, add), zip2 (xs, ys))
vsum = (xss) -> fold (vadd, xss)

neg = (x) -> -x
sub = (x, y) -> add(x, neg @ y)
vsub = (xs, ys) -> applyn (part (dewrapply, sub), zip2 (xs, ys))
vheadsubn = (xss) -> headapplyn (vsub, xss)

binand = (x, y) -> x and y
all = (xs) -> fold (binand, xs)
transeqn = (xs) -> all . headapplyn (eq, xs)

dontails = (x, f, y) -> don (pre @ x, f, f @ y)
don = (x, f, y) -> capply (eqz . head . nuple, head . tail . tail . nuple, dontails) (x, f, y)
mul = (x, y) -> don (x, part (cons, y), nil ())

s2 = (xs, ys) -> cons (head @ xs, sum (tail @ xs, ys))
sum = (xs, ys) -> capply (eqzn . head . nuple, head . tail . nuple, s2) (xs, ys)
concat = (xss) -> fold (sum, xss)

first = (f, xs) -> xs >> capply (eqzn, use0 @ nil, capply, f . head, head, part (first, f) . tail)
map = (x, yzs) -> head . tail . first (part (eq, x) . head, yzs)

un = (x) -> x >> capply (eqz, wuse0 . s . z (), wuse0 . z ())
binor = (x, y) -> un . binand (un @ x, un @ y)
lthan = (x, y) -> x < y
gtheq = (x, y) -> un . lthan (x, y)
gthan = (x, y) -> binand (gtheq (x, y), un . eq (x, y))
ltheq = (x, y) -> un . gthan (x, y)
between = (x, y) -> (w) -> binand (gtheq (w, x), ltheq (w, y))

cpoint = (x) -> ord (x)
upa = () -> cpoint ("A")
lowa = () -> cpoint ("a")
cpbtw = (x, y) -> (w) -> w >> between (cpoint @ x, cpoint @ y) . cpoint
asciilow = (x) -> cpbtw ("a", "z") @ x
asciiup = (x) -> cpbtw ("A", "Z") @ x
asciial = (x) -> binor (asciilow @ x, asciiup @ x)
cpoff = (x, y) -> sub (cpoint @ y, x)
asciioff = (x) -> x >> capply (asciiup, part (cpoff, upa ()), part (cpoff, lowa ()))

zvec = (x) -> mul (x, z ())
zvec32 = () -> mul (thirtytwo (), z ())
basisvec = (x, y) -> concat . nuple (zvec @ y, consnil . s . z (), zvec . pre . sub (x, y))
basis32 = (x) -> basisvec (thirtytwo (), x)
asciivec = (x) -> basis32 . asciioff @ x
anyvec = (x) -> x >> capply (asciial, asciivec, use0 @ zvec32)

entry = (*xs) -> transeqn . cons (zvec32 (), vheadsubn . applyn (part (vsum . applyn, anyvec), xs))
""")
