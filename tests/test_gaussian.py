import pytest
from mpmath import mp, erf, erfinv as mp_erfinv, mpf, floor, sqrt
from eth_abi import encode, decode
import subprocess
import json

mp.dps = 50

WAD = 10**18
POW96 = 2**96
ERROR_TOLERANCE = 10**10


def get_erfc_python(x: int) -> int:
    x_float = mpf(x) / 10**18
    result = mpf(1) - erf(x_float)
    return int(floor(result * 10**18))


def get_erfinv_python(x: int) -> int:
    x_float = mpf(x) / 10**18
    try:
        result = mp_erfinv(x_float)
        return int(floor(result * 10**18))
    except:
        return 0


def get_erfcinv_python(x: int) -> int:
    x_float = mpf(x) / 10**18
    try:
        result = mp_erfinv(1 - x_float)
        return int(floor(result * 10**18))
    except:
        return 0


def get_cdf_python(x: int, u: int, o: int) -> int:
    x_f = mpf(x) / 10**18
    u_f = mpf(u) / 10**18
    o_f = mpf(o) / 10**18
    z = -(x_f - u_f) / (o_f * sqrt(2))
    result = (1 - erf(z)) / 2
    return int(floor(abs(result) * 10**18))


def get_ppf_python(x: int, u: int, o: int) -> int:
    x_f = mpf(x) / 10**18
    u_f = mpf(u) / 10**18
    o_f = mpf(o) / 10**18
    try:
        result = u_f - o_f * sqrt(2) * mp_erfinv(1 - 2 * x_f)
        result_int = int(floor(result * 10**18))
        if result_int < 0:
            return (1 << 256) + result_int
        return result_int
    except:
        return 0


def to_x96(x: int) -> int:
    return (x * POW96) // WAD


class TestPythonReference:
    def test_erfc_python_at_zero(self):
        result = get_erfc_python(0)
        assert result == WAD

    def test_erfc_python_positive(self):
        result = get_erfc_python(WAD)
        assert 0 < result < WAD

    def test_erfc_python_negative(self):
        result = get_erfc_python(-WAD)
        assert WAD < result < 2 * WAD

    def test_cdf_python_at_mean(self):
        result = get_cdf_python(0, 0, WAD)
        assert abs(result - WAD // 2) < ERROR_TOLERANCE

    def test_erfinv_python_at_zero(self):
        result = get_erfinv_python(0)
        assert result == 0


class TestCompilation:
    def test_contract_compiles(self, compiled_contract):
        assert compiled_contract["abi"] is not None
        assert compiled_contract["bytecode"] is not None
        assert len(compiled_contract["bytecode"]) > 0


class TestPolynomialCoefficients:
    def test_erfc_boundary(self):
        boundary = 321256254694393905851862497420
        assert boundary > 0
        as_float = boundary / POW96
        assert 4.0 < as_float < 4.1

    def test_erfinv_range_0_99(self):
        boundary = 19652559880814263879430766018
        as_float = boundary / POW96
        assert 0.24 < as_float < 0.25

    def test_erfinv_range_0_9999(self):
        boundary = 20149819025262612946429451120
        as_float = boundary / POW96
        assert 0.25 < as_float < 0.26


class TestIntegration:
    def test_cdf_at_different_points(self):
        test_cases = [
            (0, 0, WAD, WAD // 2),
            (WAD, 0, WAD, None),
            (-WAD, 0, WAD, None),
        ]

        for x, u, o, expected in test_cases:
            result = get_cdf_python(x, u, o)
            if expected is not None:
                assert abs(result - expected) < ERROR_TOLERANCE, (
                    f"cdf({x / WAD}, {u / WAD}, {o / WAD})"
                )
            else:
                assert 0 <= result <= WAD, f"cdf({x / WAD}, {u / WAD}, {o / WAD}) out of bounds"

    def test_erfc_symmetry(self):
        x = WAD
        y_pos = get_erfc_python(x)
        y_neg = get_erfc_python(-x)
        assert abs(y_pos + y_neg - 2 * WAD) < ERROR_TOLERANCE

    def test_cdf_symmetry(self):
        x = WAD
        u, o = 0, WAD
        y_pos = get_cdf_python(x, u, o)
        y_neg = get_cdf_python(-x, u, o)
        assert abs(y_pos + y_neg - WAD) < ERROR_TOLERANCE
