# vygauss

Highly optimized Vyper library for statistical functions with error < 1e-8, including `erfc`, `erfinv`, `erfcinv`, `ppf`, and `cdf`.

Ported from [solgauss](https://github.com/cairoeth/solgauss) (Solidity).

## Installation

```sh
pip install vyper pytest titanoboa mpmath
```

## Functions

### `erfc(x: int256) -> uint256`
Complementary error function. Input scaled by 2^96, output scaled by WAD (1e18).

### `erfinv(x: int256) -> int256`
Inverse error function. Input scaled by 2^96, output scaled by WAD.

### `erfcinv(x: int256) -> int256`
Inverse complementary error function. Input in WAD, output in WAD.

### `ppf(x: int256, u: int256, o: int256) -> int256`
Percent point function (inverse CDF) of normal distribution.
- `x`: probability in WAD (0 < x < 1)
- `u`: mean in WAD
- `o`: standard deviation in WAD

### `cdf(x: int256, u: int256, o: uint256) -> uint256`
Cumulative distribution function of normal distribution.
- `x`: value to evaluate in WAD
- `u`: mean in WAD
- `o`: standard deviation in WAD
- Returns: cumulative probability in WAD (0 to 1)

## Testing

```sh
cd vygauss
python3 -m pytest tests/ -v
```

Tests use [mpmath](https://mpmath.org/) for high-precision reference implementations.

## Acknowledgements

- [solgauss](https://github.com/cairoeth/solgauss) - Original Solidity implementation
- [gud-cdf](https://github.com/Philogy/gud-cdf) - Codification methodology
- [Rational Chebyshev Approximation](https://link.springer.com/article/10.1007/BF02162506)
