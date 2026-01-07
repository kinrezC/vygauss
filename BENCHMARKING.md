# Gas Benchmarking

## Measurement Methodology

titanoboa measures **external function calls**, which include ~118 gas overhead (CALL opcode + context setup). Foundry measures **library functions** with minimal overhead.

To compare fairly: subtract 118 gas from titanoboa results.

## Measuring Call Overhead

```bash
python3 scripts/compute_boa_call_overhead.py
```

This measures the overhead by calling a no-op function:
- `noop()` (no computation) = 118 gas
- `simple_computation()` = 308 gas
- Pure computation = 308 - 118 = 190 gas

## Running Benchmarks

```bash
python3 scripts/gas_benchmark.py
```

Compares standard Vyper vs Venom compiler vs solgauss baseline.

## Example Comparison

```
erfc (titanoboa):  735 gas (Venom)
Pure computation:  735 - 118 = 617 gas
solgauss:          688 gas
Ratio:             617 / 688 = 0.90x (10% faster)
```

## Files

- `scripts/gas_benchmark.py` - Main benchmark comparing standard/Venom/Solidity
- `scripts/compute_boa_call_overhead.py` - Measures the 118 gas constant

## References

- [solgauss](https://github.com/cairoeth/solgauss) - Solidity reference implementation
