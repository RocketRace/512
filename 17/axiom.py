from __future__ import division                                                                                                                                                                                                         ;print('J')

# O((n^2)^(n^2)) primer algorithm
# runs very fast for n < 3
# like comment and subscribe for fast algorithms
# free tibet

import functools, itertools, operator
from tqdm import tqdm

entry = lambda n: (
    lambda Def = lambda x, **s: {setattr(x, n, y) for (n, y) in s.items()}.clear(),
           new = type('new', (), dict(__getattr__ = lambda _, t: lambda **s: type(t, (), s))
    )(): (
        lambda op = new.op(
            __init__ = lambda o, f: Def(o, f=f),
            __ror__ = lambda o, a: new._(
                __init__ = lambda o, f, a: Def(o, f=f, a=a),
                __or__ = lambda o, b: o(o.a, b),
                __call__ = lambda o, a, b: o.f(a, b),
            )(o.f, a),
        ): (
            lambda ᐱ = op(pow),
                   ᆢᆢ = op(getattr),
                   ᆖ = op(operator.eq),
                   ᔓ  = op(range),
                   Σ = op(
                       lambda p, a: (
                           lambda f: (lambda x: f(lambda a: x(x)(a)))(lambda x: f(lambda a: x(x)(a)))
                        )(
                            lambda f: lambda a: (lambda q, w: q if w == 1 else q + f((q, w - 1)))(*a)
                        )((a, p))
            ): (
                lambda method = new.method(__getattr__ = lambda _, m: op(lambda a, b: (a |ᆢᆢ| m)(b)))(), 
                       set = new.set(
                           __init__ = lambda S, it, dims=1: (
                               lambda inner = tuple(it): Def(S, inner=inner, d=dims)
                           )(),
                           __pow__ = lambda S, n: itertools.product(S.inner, repeat=n),
                           __call__ = lambda S, *xs: S.inner[
                               functools.reduce(lambda a, x: a * round(len(S.inner) |ᐱ| 1 / S.d) + x, xs, 0)
                           ],
                           Each = lambda S, f: {f(e) for e in S.inner}.clear(),
                           quant = lambda S, f: lambda g: f(g(*xs) for xs in S |ᐱ| g.__code__.co_argcount),
                ): (
                    lambda quant = method.quant, Each = method.Each: (
                        lambda quantified = lambda f: op(lambda S, g: (S |quant| f)(g)): (
                            lambda Ɐ = quantified(all), Ǝ = quantified(any): (
                                lambda field = lambda S, 十, ᐧ : (
                                    lambda 十 = set(十, 2), ᐧ = set( ᐧ , 2): (
                                        lambda R = set(1 |ᔓ| n + 1): (
                                            S |Each| (lambda e: e.Promote(十, ᐧ )) or new.structure(
                                                __bool__ = lambda _: (
                                                        S |Ɐ| (lambda a, b: a + b == b + a)
                                                    and S |Ɐ| (lambda a, b: a * b == b * a)
                                                    and S |Ɐ| (lambda a, b, c: (a + b) + c == a + (b + c))
                                                    and S |Ɐ| (lambda a, b, c: (a * b) * c == a * (b * c))
                                                    and S |Ɐ| (lambda a, b, c: a * (b + c) == a * b + a * c)
                                                    and S |Ǝ| (lambda Ø: (
                                                        S |Ǝ| (lambda 𐑑: (Ø != 𐑑
                                                    and S |Ɐ| (lambda a: a + Ø == a)
                                                    and S |Ɐ| (lambda a: a * 𐑑 == a)
                                                    and S |Ɐ| (lambda a: (
                                                        S |Ǝ| (lambda ｰa: a + ｰa == Ø)))
                                                    and S |Ɐ| (lambda a: (a == Ø
                                                     or S |Ǝ| (lambda a̕: a * a̕ == 𐑑)))
                                                    and R |Ɐ| (lambda p: (p == n) |ᆖ| (p |Σ| 𐑑 == Ø))
                                                )))))
                                            )()
                                        )
                                    )() 
                                )(): (
                                    lambda element = new.element(
                                        __init__ = lambda a, i: Def(a, i=i),
                                        __add__ = lambda a, b: a.十(a.i, b.i),
                                        __mul__ = lambda a, b: a. ᐧ (a.i, b.i),
                                        Promote = lambda a, 十, ᐧ : Def(a, 十 = 十, ᐧ = ᐧ ),
                                    ): (
                                        lambda S = set(element(i) for i in 0 |ᔓ| n): (
                                            any(tqdm((
                                                field(S, 十, ᐧ )
                                                for 十 in S |ᐱ| (n |ᐱ| 2)
                                                for ᐧ  in S |ᐱ| (n |ᐱ| 2)
                                            ), unit=" structures", total=(n |ᐱ| 2) |ᐱ| (n |ᐱ| 2)))
                                        )
                                    )()
                                )() 
                            )()
                        )()
                    )()
                )()
            )()  
        )()
    )()
)()
