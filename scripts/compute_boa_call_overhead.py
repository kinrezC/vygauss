#!/usr/bin/env python3
"""
Measure external call overhead in titanoboa.

titanoboa measures external calls; Foundry measures library functions.
This script measures the constant overhead (~118 gas) to subtract from
titanoboa results for fair comparison.
"""

import boa
import statistics
from pathlib import Path


def measure_call_overhead():
    """Measure external call overhead in titanoboa."""

    # Create minimal test contract
    source = """
@external
@pure
def noop() -> uint256:
    return 0

@external
@pure
def simple_computation() -> uint256:
    x: uint256 = 42
    y: uint256 = 123
    z: uint256 = x * y + x // y
    return z
"""

    contract = boa.loads(source)

    # Measure baseline (noop)
    print("Measuring external call overhead in titanoboa...")
    print()

    results = []
    for _ in range(10):
        contract.noop()
        results.append(contract._computation.get_gas_used())

    baseline = int(statistics.mean(results))
    baseline_min = min(results)
    baseline_max = max(results)

    print("noop() - External function with no computation:")
    print(f"  avg: {baseline}, min: {baseline_min}, max: {baseline_max}")
    print()

    # Measure with computation
    results = []
    for _ in range(10):
        contract.simple_computation()
        results.append(contract._computation.get_gas_used())

    with_comp = int(statistics.mean(results))
    comp_cost = with_comp - baseline

    print("simple_computation() - External function with computation:")
    print(f"  avg: {with_comp}, computation cost: {comp_cost}")
    print()

    print("=" * 70)
    print("RESULT: External call overhead in titanoboa")
    print("=" * 70)
    print(f"Call overhead: {baseline} gas")
    print()
    print("HOW TO USE:")
    print(f"  pure_computation_cost = titanoboa_total - {baseline}")
    print()
    print("EXAMPLE:")
    print(f"  erfc (titanoboa): 1030 gas total")
    print(f"  erfc (pure comp): 1030 - {baseline} = {1030 - baseline} gas")
    print()
    print("COMPARISON:")
    print(f"  solgauss (Foundry): 688 gas (already pure computation)")
    print(f"  vygauss (titanoboa): {1030 - baseline} gas (after subtracting overhead)")
    print()

    return baseline


if __name__ == "__main__":
    overhead = measure_call_overhead()

    # Write the constant to a file so other scripts can use it
    overhead_file = Path(__file__).parent / ".boa_call_overhead"
    overhead_file.write_text(str(overhead))
    print(f"Overhead value saved to {overhead_file}")
