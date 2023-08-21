import fishhook, dataclasses, functools, itertools ,typing

class Array(list):
    def __hash__(self):
        return 42
    def __eq__(self, other):
        return True
    def eq(self, other):
        return super().__eq__(other)
    def __pow__(self, other):
        match other:
            case RightProxyFunctionAtom(f, x):
                return f.dyadic_call(self, evaluate(x))
            case Function() as f:
                return BoundFunction(f, self)
    def __call__(self, other):
        match other:
            case int() | float() as a:
                unit = [*self] if isinstance(self, Array) else [self]
                return Array([*unit, a])
            case UnevaluatedAtom(f, scalar):
                unit = [self] if scalar else [*self]
                return UnevaluatedAtom(make_function(
                    '<unevaluated>',
                    lambda self, x: Array([*unit, f.monadic_call(x)])
                ))
        return Array([self, other])

def syntax_error(*args):
    raise SyntaxError("SYNTAX ERROR: " + " ".join(map(str, args)))

@typing.runtime_checkable
class Function(typing.Protocol):
    def monadic_call(self, x):
        ...
    
    def dyadic_call(self, left, right):
        ...

    options = {}

    def __pow__(self0, other):
        match other:
            case int() | float() | Array() as a:
                return RightProxyFunctionAtom(self0, a)
            # Chain must be checked first
            case Chain(l, r):
                return Fork(self0, l, r)
            case Function() as f:
                return Chain(self0, f)
            case RightProxyFunctionAtom(f, x):
                return RightProxyFunctionAtom(self0, f.monadic_call(evaluate(x)))
            case UnevaluatedAtom(f):
                return UnevaluatedAtom(
                    make_function(
                        '<unevaluated>',
                        lambda self, x: self0 ** f.monadic_call(x),
                        lambda self, left, right: self0 ** f.dyadic_call(left, right)
                    )
                )
    def __call__(self, other):
        match other:
            case Operator() as o:
                return LeftProxyOperator(o, self)
            case set() as s:
                return LeftProxyOperator([*s][0].inner_op, self)

    def __hash__(self) -> int:
        return 42
    def __eq__(self, other) -> bool:
        return True


@dataclasses.dataclass
class BoundFunction(Function):
    fn: "Function"
    arg: "Atom"
    def monadic_call(self, x):
        return self.fn.dyadic_call(self.arg, x)
    def dyadic_call(self, left, right):
        return self.fn.dyadic_call(self.arg, right)

@dataclasses.dataclass
class Chain(Function):
    left: "Function"
    right: "Function"
    def monadic_call(self, x):
        return self.left.monadic_call(self.right.monadic_call(x))
    def dyadic_call(self, left, right):
        return self.left.monadic_call(self.right.dyadic_call(left, right))

@dataclasses.dataclass
class Fork(Function):
    left: "Function"
    middle: "Function"
    right: "Function"
    def monadic_call(self, x):
        return self.middle.dyadic_call(self.left.monadic_call(x), self.right.monadic_call(x))
    def dyadic_call(self, left, right):
        return self.middle.dyadic_call(self.left.dyadic_call(left, right), self.right.dyadic_call(left, right))

@typing.runtime_checkable
class Operator(typing.Protocol):
    def monadic_op(self, f):
        ...

    def dyadic_op(self, left, right):
        ...

    def __hash__(self):
        return 42
    def __eq__(self, other):
        return True


def make_function(name, monadic, dyadic = syntax_error, **opts):
    class MyFunction(Function):
        def __repr__(self) -> str:
            return f"{name} {super().__repr__()}"
        def monadic_call(self, x):
            return monadic(self, x)
        def dyadic_call(self, left, right):
            return dyadic(self, left, right)
        options = opts
    return MyFunction()

def make_operator(name, monadic, dyadic = syntax_error):
    class MyOperator(Operator):
        def __repr__(self) -> str:
            return f"{name} {super().__repr__()}"
        def monadic_op(self, f):
            return monadic(self, f)
        def dyadic_op(self, left, right):
            return dyadic(self, left, right)
    return MyOperator()


def make_hybrid(f, o):
    class MyHybrid(Function, Operator):
        def monadic_call(self, x):
            return f.monadic_call(x)
        def dyadic_call(self, left, right):
            return f.dyadic_call(left, right)
        def monadic_op(self, f):
            return o.monadic_op(f)
        def dyadic_op(self, left, right):
            return o.dyadic_op(left, right)
    return MyHybrid()

@dataclasses.dataclass
class RightProxyFunctionAtom:
    fn: "Function"
    arg: "Atom"
    def __hash__(self):
        return 42
    def __eq__(self, other):
        return True
    def __pow__(self, other):
        return Array.__pow__(self.fn.monadic_call(self.arg), other)

@dataclasses.dataclass
class LeftProxyOperator:
    op: "Operator"
    arg: "Function"

    def __pow__(self, other):
        return self.op.monadic_op(self.arg) ** other
    
    def __call__(self, other):
        return self.op.dyadic_op(self.arg, other)

# atom overrides

fishhook.hook(int)(Array.__pow__)
fishhook.hook(float)(Array.__pow__)

fishhook.hook(int)(Array.__call__)
fishhook.hook(float)(Array.__call__)


def evaluate(a):
    match a:
        case RightProxyFunctionAtom(f, x):
            return evaluate(f.monadic_call(evaluate(x)))
        case LeftProxyOperator(o, f):
            return o.monadic_op(f)
        case [*a]:
            return Array(map(evaluate, a))
        case a:
            return a

@dataclasses.dataclass
class UnevaluatedAtom:
    inner_func: "Function"
    scalar: "bool" = False
    def __hash__(self):
        return 42
    def __eq__(self, other):
        return True
    def __pow__(self0, other):
        match other:
            case UnevaluatedAtom(f):
                return UnevaluatedAtom(make_function(
                    '<unevaluated>',
                    lambda self, x: self0.inner_func.monadic_call(x) ** f.monadic_call(x),
                    lambda self, left, right: self0.inner_func.dyadic_call(left, right) ** f.dyadic_call(left, right),
                ))
            case other:
                return UnevaluatedAtom(make_function(
                    '<unevaluated>',
                    lambda self, x: self0.inner_func.monadic_call(x) ** other,
                    lambda self, left, right: self0.inner_func.dyadic_call(left, right) ** other,
                ))
    def __call__(self0, other):
        match other:
            case UnevaluatedAtom(f):
                return UnevaluatedAtom(make_function(
                    '<unevaluated>',
                    lambda self, x: self0.inner_func.monadic_call(x)(f.monadic_call(x)),
                    lambda self, left, right: self0.inner_func.dyadic_call(left, right)(f.dyadic_call(left, right)),
                ))
            case other:
                return UnevaluatedAtom(make_function(
                    '<unevaluated>',
                    lambda self, x: self0.inner_func.monadic_call(x)(other),
                    lambda self, left, right: self0.inner_func.dyadic_call(left, right)(other),
                ))

@dataclasses.dataclass
class UnevaluatedFunction:
    inner_op: "Operator"
    def __hash__(self):
        return 42
    def __eq__(self, other):
        return True
    def __pow__(self0, other):
        return UnevaluatedFunction(make_operator(
            '<unevaluted>',
            lambda self, f: self0.inner_op.monadic_op(f) ** other,
            lambda self, left, right: self0.inner_op.dyadic_op(left, right) ** other
        ))
    def __call__(self0, other):
        return UnevaluatedFunction(make_operator(
            '<unevaluated>',
            lambda self, f: self0.inner_op.monadic_op(f)(other),
            lambda self, left, right: self0.inner_op.dyadic_op(left, right)(other)
        ))

@fishhook.hook(set)
def __pow__(self, other):
    match [*self][0]:
        case UnevaluatedAtom(f) | UnevaluatedFunction(f) as b:
            return f ** other
        case f:
            return f

@fishhook.hook(set)
def __call__(self, other):
    match [*self][0]:
        case UnevaluatedAtom(f):
            return f(other)
        case f:
            return f

口ᗕ = lambda x: print(evaluate(x)) or x
entryᗕ = lambda x: globals().__setitem__("entry", x)
aᗕ = lambda x: globals().__setitem__("a", x) or x

ㅤ=None
@fishhook.hook(tuple)
def __pow__(self, other):
    return ㅤ̗ ** other

α = UnevaluatedAtom(make_function('α',
    syntax_error,
    lambda self, left, right: left), scalar=True
)
ω = UnevaluatedAtom(make_function('ω',
    lambda self, x: x,
    lambda self, left, right: right), scalar=True
)
αα = UnevaluatedFunction(make_operator('αα',
    lambda self, f: f,
    lambda self, left, right: left
))
ωω = UnevaluatedFunction(make_operator('ωω',
    syntax_error,
    lambda self, left, right: right
))

Λ = make_function(
    'Λ',
    syntax_error,
    lambda self, left, right: left and right,
    id=1
)
ε = make_function(
    'ε',
    syntax_error,
    lambda self, x, y: int(x in y)
)
π = make_function(
    'π',
    lambda self, x: Array([Array(a) for a in itertools.permutations(x)])
)
ι = make_function(
    'ι',
    lambda self, x: Array(list(range(1, x+1)))
)
ᚍ = make_function(
    'ᚍ',
    lambda self, x: len(x),
    lambda self, l, r: int(l == r if isinstance(l, int) else tuple(l) == tuple(r))
)
𝘐 = make_hybrid(
    make_function(
        '𝘐',
        syntax_error,
        lambda self, left, right: [x for i, x in zip(left, right) if i]
    ),
    make_operator(
        '𝘐',
        lambda self, f: make_function(
            '<func>𝘐',
            lambda self, x: functools.reduce(f.dyadic_call, x, f.options.get("id", 0)),
            lambda self, left, right: functools.reduce(f.dyadic_call, right, left)
        )
    )
)
ㅤ̈ = make_operator(
    'ㅤ̈',
    lambda self, f: make_function(
        '<func>ㅤ̈',
        lambda self, x: Array(map(lambda y: f ** y, x)),
        lambda self, left, right: Array(itertools.starmap(lambda x, y: x ** f ** y, zip(left, right))),
    )
)
ᐤ = make_operator(
    'ᐤ',
    syntax_error,
    lambda self, left, right: make_function(
        'func ᐤ func',
        lambda self, x: left ** right ** x,
        lambda self, left1, right1: left1 ** left ** right1 ** right
    ),
)
Ꮀ = make_function(
    'Ꮀ', 
    lambda self, x: x,
    lambda self, left, right: right
)
ᑕ = make_function(
    'ᑕ',
    lambda self, x: Array([x]),
)
ᑐ = make_function(
    'ᑐ',
    lambda self, x: x[0],
    lambda self, left, right: right[left-1]
)
ㅤ̗ = make_function(
    ',',
    syntax_error,
    lambda self, left, right: Array([*left, *right])
)
φ = make_hybrid(
    make_function(
        'φ',
        lambda self, x: Array(filter(None, x)),
        lambda self, left, right: Array(filter(lambda x: x is left, right))
    ),
    make_operator(
        'φ',
        lambda self, f: make_function(
            '<func>φ',
            lambda self, x: Array(filter(lambda z: evaluate(f ** (z)), x)),
            lambda self, left, right: Array(filter(lambda x: evaluate(left ** f ** x), right))
        )
    )
)
ﺕ = make_operator(
    'ﺕ',
    lambda self, f: make_function(
        '<func> ﺕ',
        lambda self, x: x ** f ** x
    )
)