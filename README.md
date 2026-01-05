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

## Gas Benchmarks

Run benchmarks: `python3 scripts/gas_benchmark.py`

### Comparison: vygauss (Vyper) vs solgauss (Solidity)

| Function | vygauss (min) | vygauss (max) | solgauss (min) | solgauss (max) | Overhead |
|----------|---------------|---------------|----------------|----------------|----------|
| erfc     | 2688          | 2736          | 649            | 693            | ~4x      |
| erfinv   | 1643          | 7670          | 647            | 1670           | ~2.5-4.5x|
| erfcinv  | 2860          | 7774          | 710            | 723            | ~4-10x   |
| cdf      | 2997          | 3045          | 731            | 754            | ~4x      |
| ppf      | 2105          | 3218          | 814            | 859            | ~2.5-4x  |

### vygauss Detailed Benchmarks

| Function              | min  | max  | avg  | median |
|-----------------------|------|------|------|--------|
| erfc                  | 2688 | 2736 | 2702 | 2688   |
| erfinv (Range 1)      | 2717 | 2756 | 2723 | 2717   |
| erfinv (Range 2)      | 1643 | 1682 | 1662 | 1662   |
| erfinv (Range 3)      | 7631 | 7670 | 7638 | 7631   |
| erfcinv               | 2860 | 7774 | 3578 | 2899   |
| cdf                   | 2997 | 3045 | 3024 | 3045   |
| ppf                   | 2105 | 3218 | 2888 | 3179   |

The gas overhead compared to Solidity is due to:
- Vyper's lack of inline assembly support
- Additional safety checks in Vyper
- Less aggressive compiler optimizations

For gas-critical applications, consider using [solgauss](https://github.com/cairoeth/solgauss). For Vyper-native projects prioritizing code readability and safety, vygauss provides functionally equivalent results.

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
