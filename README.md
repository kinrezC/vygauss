# vygauss

Vyper library for statistical functions with error < 1e-8, including `erfc`, `erfinv`, `erfcinv`, `ppf`, and `cdf`.

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

Run: `python3 scripts/gas_benchmark.py`

### Comparison with solgauss (Solidity)

titanoboa measures external calls (~118 gas overhead). Values below are pure computation costs (total - 118). See `BENCHMARKING.md` for methodology.

| Function | solgauss | std | std vs sol | Venom | Venom vs sol |
|----------|----------|-----|------------|-------|--------------|
| erfc     | 688      | 912 | +33%       | 617   | **-10%**     |
| erfcinv  | 828      | 1291| +56%       | 893   | +8%          |
| cdf      | 610      | 1234| +102%      | 866   | +42%         |
| ppf      | 2001     | 1222| -39%       | 933   | **-53%**     |

### Detailed Benchmarks (Venom, total gas including call overhead)

| Function | min | max | avg | median |
|----------|-----|-----|-----|--------|
| erfc | 727 | 755 | 735 | 727 |
| erfinv (Range 1) | 675 | 705 | 680 | 675 |
| erfinv (Range 2) | 572 | 602 | 587 | 587 |
| erfinv (Range 3) | 2265 | 2295 | 2271 | 2265 |
| erfcinv | 771 | 2361 | 1011 | 801 |
| cdf | 968 | 996 | 984 | 996 |
| ppf | 965 | 1098 | 1051 | 1068 |

### Optimization Techniques

1. **`unsafe_*` operations** - Bypass Vyper's overflow checks where input bounds are proven safe (matches Solidity assembly semantics). 56-66% reduction from baseline.

2. **Venom compiler** (`--experimental-codegen`) - IR-level optimizations that reduce redundant checks. Additional 22-30% reduction.

```python
import boa
gaussian = boa.loads(source, compiler_args={'experimental_codegen': True})
```

For Vyper projects, vygauss with Venom provides competitive gas performance. For maximum efficiency in multi-language systems, use [solgauss](https://github.com/cairoeth/solgauss).

## Testing

```sh
python3 -m pytest tests/ -v
```

Tests use [mpmath](https://mpmath.org/) for high-precision reference values.

## Acknowledgements

- [solgauss](https://github.com/cairoeth/solgauss) - Original Solidity implementation
- [gud-cdf](https://github.com/Philogy/gud-cdf) - Codification methodology
- [Rational Chebyshev Approximation](https://link.springer.com/article/10.1007/BF02162506)
