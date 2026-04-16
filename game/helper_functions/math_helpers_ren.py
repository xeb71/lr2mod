from __future__ import annotations
"""renpy
IF FLAG_OPT_IN_ANNOTATIONS:
    rpy python annotations
init -49 python:
"""
import math as _pmath

# A store-visible math namespace that shadows Python's math module.
# All functions are defined inline as lambdas so they can be used
# in Ren'Py expressions without importing Python's math module directly.
# Programs that need math can do: math.sin(x), math.tan(x), etc.

class math:
    # Trigonometric functions
    sin       = staticmethod(lambda x: _pmath.sin(x))
    cos       = staticmethod(lambda x: _pmath.cos(x))
    tan       = staticmethod(lambda x: _pmath.tan(x))
    asin      = staticmethod(lambda x: _pmath.asin(x))
    acos      = staticmethod(lambda x: _pmath.acos(x))
    atan      = staticmethod(lambda x: _pmath.atan(x))
    atan2     = staticmethod(lambda y, x: _pmath.atan2(y, x))

    # Hyperbolic functions
    sinh      = staticmethod(lambda x: _pmath.sinh(x))
    cosh      = staticmethod(lambda x: _pmath.cosh(x))
    tanh      = staticmethod(lambda x: _pmath.tanh(x))

    # Rounding and integer helpers
    floor     = staticmethod(lambda x: _pmath.floor(x))
    ceil      = staticmethod(lambda x: _pmath.ceil(x))
    trunc     = staticmethod(lambda x: _pmath.trunc(x))

    # Powers and roots
    sqrt      = staticmethod(lambda x: _pmath.sqrt(x))
    pow       = staticmethod(lambda x, y: _pmath.pow(x, y))
    exp       = staticmethod(lambda x: _pmath.exp(x))

    # Absolute value
    fabs      = staticmethod(lambda x: _pmath.fabs(x))

    # Logarithms
    log       = staticmethod(lambda x, *args: _pmath.log(x, *args))
    log2      = staticmethod(lambda x: _pmath.log2(x))
    log10     = staticmethod(lambda x: _pmath.log10(x))

    # Angle conversion
    radians   = staticmethod(lambda x: _pmath.radians(x))
    degrees   = staticmethod(lambda x: _pmath.degrees(x))

    # Other common functions
    hypot     = staticmethod(lambda *args: _pmath.hypot(*args))
    gcd       = staticmethod(lambda a, b: _pmath.gcd(a, b))
    isfinite  = staticmethod(lambda x: _pmath.isfinite(x))
    isinf     = staticmethod(lambda x: _pmath.isinf(x))
    isnan     = staticmethod(lambda x: _pmath.isnan(x))

    # Constants
    pi    = _pmath.pi
    e     = _pmath.e
    tau   = _pmath.tau
    inf   = _pmath.inf
    nan   = _pmath.nan
