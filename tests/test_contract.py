import pytest
import boa
from mpmath import mp, erf, erfinv as mp_erfinv, mpf, floor, sqrt
from pathlib import Path

mp.dps = 50

WAD = 10**18
POW96 = 2**96
ERROR_TOLERANCE = 10**10


def get_erfc_python(x_wad: int) -> int:
    x_float = mpf(x_wad) / 10**18
    result = mpf(1) - erf(x_float)
    return int(floor(result * 10**18))


def get_cdf_python(x: int, u: int, o: int) -> int:
    x_f = mpf(x) / 10**18
    u_f = mpf(u) / 10**18
    o_f = mpf(o) / 10**18
    z = -(x_f - u_f) / (o_f * sqrt(2))
    result = (1 - erf(z)) / 2
    return int(floor(abs(result) * 10**18))


def to_x96(x_wad: int) -> int:
    return (x_wad * POW96) // WAD


def from_signed_int256(val: int) -> int:
    if val > (1 << 255):
        return val - (1 << 256)
    return val


@pytest.fixture(scope="module")
def gaussian():
    contract_path = Path(__file__).parent.parent / "src" / "gaussian.vy"
    return boa.load(str(contract_path))


class TestErfc:
    @pytest.mark.parametrize(
        "x_wad",
        [
            0,
            WAD // 10,
            WAD // 2,
            WAD,
            2 * WAD,
            3 * WAD,
            -WAD // 10,
            -WAD,
            -2 * WAD,
        ],
    )
    def test_erfc_known_values(self, gaussian, x_wad):
        x_96 = to_x96(x_wad)
        actual = gaussian.erfc(x_96)
        expected = get_erfc_python(x_wad)

        error = abs(actual - expected)
        assert error < ERROR_TOLERANCE, f"erfc({x_wad / WAD}) error {error} >= {ERROR_TOLERANCE}"

    def test_erfc_at_zero_is_one(self, gaussian):
        actual = gaussian.erfc(0)
        assert abs(actual - WAD) < ERROR_TOLERANCE

    def test_erfc_symmetry(self, gaussian):
        x_96 = to_x96(WAD)
        y_pos = gaussian.erfc(x_96)
        y_neg = gaussian.erfc(-x_96)

        assert abs(y_pos + y_neg - 2 * WAD) < ERROR_TOLERANCE

    def test_erfc_large_positive_is_near_zero(self, gaussian):
        x_96 = to_x96(5 * WAD)
        actual = gaussian.erfc(x_96)
        assert actual < ERROR_TOLERANCE

    def test_erfc_large_negative_is_near_two(self, gaussian):
        x_96 = to_x96(-5 * WAD)
        actual = gaussian.erfc(x_96)
        assert abs(actual - 2 * WAD) < ERROR_TOLERANCE


class TestCdf:
    @pytest.mark.parametrize(
        "x,u,o",
        [
            (0, 0, WAD),
            (WAD, 0, WAD),
            (-WAD, 0, WAD),
            (2 * WAD, WAD, WAD),
            (0, -WAD, 2 * WAD),
        ],
    )
    def test_cdf_known_values(self, gaussian, x, u, o):
        actual = gaussian.cdf(x, u, o)
        expected = get_cdf_python(x, u, o)

        error = abs(actual - expected)
        assert error < ERROR_TOLERANCE, (
            f"cdf({x / WAD}, {u / WAD}, {o / WAD}) error {error} >= {ERROR_TOLERANCE}"
        )

    def test_cdf_at_mean_is_half(self, gaussian):
        actual = gaussian.cdf(0, 0, WAD)
        assert abs(actual - WAD // 2) < ERROR_TOLERANCE

    def test_cdf_symmetry(self, gaussian):
        y_pos = gaussian.cdf(WAD, 0, WAD)
        y_neg = gaussian.cdf(-WAD, 0, WAD)

        assert abs(y_pos + y_neg - WAD) < ERROR_TOLERANCE

    def test_cdf_range(self, gaussian):
        for x in [0, WAD, -WAD, 2 * WAD, -2 * WAD]:
            result = gaussian.cdf(x, 0, WAD)
            assert 0 <= result <= WAD, f"cdf({x / WAD}) = {result / WAD} out of [0,1]"

    def test_cdf_monotonic(self, gaussian):
        prev = 0
        for x in range(-3 * WAD, 3 * WAD + 1, WAD // 2):
            result = gaussian.cdf(x, 0, WAD)
            assert result >= prev - ERROR_TOLERANCE, f"cdf not monotonic at x={x / WAD}"
            prev = result


class TestErfinv:
    @pytest.mark.parametrize(
        "x_wad",
        [
            0,
            WAD // 10,
            WAD // 2,
            9 * WAD // 10,
            -WAD // 10,
            -WAD // 2,
            -9 * WAD // 10,
        ],
    )
    def test_erfinv_known_values(self, gaussian, x_wad):
        x_96 = to_x96(x_wad)
        actual = from_signed_int256(gaussian.erfinv(x_96))

        x_float = mpf(x_wad) / 10**18
        try:
            expected = int(floor(mp_erfinv(x_float) * 10**18))
        except:
            expected = 0

        error = abs(actual - expected)
        assert error < ERROR_TOLERANCE, f"erfinv({x_wad / WAD}) error {error} >= {ERROR_TOLERANCE}"

    def test_erfinv_at_zero(self, gaussian):
        actual = from_signed_int256(gaussian.erfinv(0))
        assert abs(actual) < ERROR_TOLERANCE

    def test_erfinv_antisymmetry(self, gaussian):
        x_96 = to_x96(WAD // 2)
        y_pos = from_signed_int256(gaussian.erfinv(x_96))
        y_neg = from_signed_int256(gaussian.erfinv(-x_96))

        assert abs(y_pos + y_neg) < ERROR_TOLERANCE


class TestErfcinv:
    @pytest.mark.parametrize(
        "x_wad",
        [
            WAD,
            WAD + WAD // 10,
            WAD // 2,
            3 * WAD // 2,
        ],
    )
    def test_erfcinv_known_values(self, gaussian, x_wad):
        actual = from_signed_int256(gaussian.erfcinv(x_wad))

        x_float = mpf(x_wad) / 10**18
        try:
            expected = int(floor(mp_erfinv(1 - x_float) * 10**18))
        except:
            expected = 0

        error = abs(actual - expected)
        assert error < ERROR_TOLERANCE, f"erfcinv({x_wad / WAD}) error {error} >= {ERROR_TOLERANCE}"

    def test_erfcinv_at_one(self, gaussian):
        actual = from_signed_int256(gaussian.erfcinv(WAD))
        assert abs(actual) < ERROR_TOLERANCE


class TestPpf:
    def test_ppf_at_half_is_mean(self, gaussian):
        actual = from_signed_int256(gaussian.ppf(WAD // 2, 0, WAD))
        assert abs(actual) < ERROR_TOLERANCE * 10

    def test_ppf_symmetry(self, gaussian):
        y_low = from_signed_int256(gaussian.ppf(WAD // 4, 0, WAD))
        y_high = from_signed_int256(gaussian.ppf(3 * WAD // 4, 0, WAD))

        assert abs(y_low + y_high) < ERROR_TOLERANCE * 10


class TestCdfPpfInverse:
    def test_cdf_ppf_roundtrip(self, gaussian):
        u, o = 0, WAD
        for p in [WAD // 4, WAD // 2, 3 * WAD // 4]:
            x = from_signed_int256(gaussian.ppf(p, u, o))
            p_back = gaussian.cdf(x, u, o)

            error = abs(p_back - p)
            assert error < ERROR_TOLERANCE * 100, (
                f"cdf(ppf({p / WAD})) != {p / WAD}, got {p_back / WAD}"
            )
