from pydantic import BaseModel
from decimal import *
from fxpmath import Fxp
from typing import Type
from fractions import Fraction

# getcontext().prec = 150

FloatingPoint = Decimal
# FixedPoint = Type[Fxp(None, signed=True, n_int=256, n_frac=18)]
FixedPoint = Decimal
FixedOrFloatFraction = Fraction


class FloatingPointUnstakeTKN(BaseModel):
    a: FloatingPoint
    b: FloatingPoint
    c: FloatingPoint
    e: FloatingPoint
    m: FixedOrFloatFraction
    n: FixedOrFloatFraction
    x: FloatingPoint
    w: FloatingPoint
    staked_bnt: FloatingPoint
    bnbnt_supply: FloatingPoint

    class Config:
        arbitrary_types_allowed = True

class FixedPointUnstakeTKN(BaseModel):
    a: FixedPoint
    b: FixedPoint
    c: FixedPoint
    e: FixedPoint
    m: FixedOrFloatFraction
    n: FixedOrFloatFraction
    x: FixedPoint
    w: FixedPoint
    staked_bnt: FixedPoint
    bnbnt_supply: FixedPoint

    class Config:
        arbitrary_types_allowed = True

# FixedPoint = Type[Fxp(None, signed=True, n_int=256, n_frac=18)]

class FixedPointGeneral(BaseModel):
    val: FixedPoint

class FloatingPointGeneral(BaseModel):
    val: FloatingPoint

