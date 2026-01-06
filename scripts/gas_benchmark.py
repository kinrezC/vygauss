#!/usr/bin/env python3
"""
Gas benchmark for vygauss.

Compares standard Vyper vs Venom compiler vs solgauss (Solidity) baseline.

titanoboa measures external calls (~118 gas overhead). Subtract this from
results before comparing with Foundry. See compute_boa_call_overhead.py.
"""

import boa
from pathlib import Path
import statistics

WAD = 10**18
POW96 = 2**96

# solgauss (Solidity) baseline from their README
SOLGAUSS_BASELINE = {
    'erfc': 688,
    'erfinv': 749,
    'erfcinv': 828,
    'cdf': 610,
    'ppf': 2001,
}

# External call overhead in titanoboa (measured constant)
# To get pure computation cost: total_gas - CALL_OVERHEAD
CALL_OVERHEAD = 118


def to_x96(x_wad: int) -> int:
    return (x_wad << 96) // WAD


def benchmark_gaussian(experimental_codegen: bool = False):
    """Benchmark vygauss with optional Venom compiler."""
    contract_path = Path(__file__).parent.parent / "src" / "gaussian.vy"
    source = contract_path.read_text()

    # Load with optional experimental codegen (Venom)
    gaussian = boa.loads(
        source,
        name="gaussian_benchmark",
        compiler_args={'experimental_codegen': experimental_codegen}
    )

    results = {}

    # erfc
    erfc_inputs = [
        to_x96(0),
        to_x96(WAD // 10),
        to_x96(WAD // 2),
        to_x96(WAD),
        to_x96(2 * WAD),
        to_x96(3 * WAD),
        to_x96(4 * WAD),
        to_x96(-WAD // 10),
        to_x96(-WAD),
        to_x96(-2 * WAD),
    ]

    gas_data = []
    for x in erfc_inputs:
        gaussian.erfc(x)
        gas_data.append(gaussian._computation.get_gas_used())
    results['erfc'] = {
        'min': min(gas_data),
        'max': max(gas_data),
        'avg': int(statistics.mean(gas_data)),
        'median': int(statistics.median(gas_data)),
    }

    # erfinv range 1
    erfinv_r1_inputs = [
        to_x96(0),
        to_x96(WAD // 10),
        to_x96(WAD // 2),
        to_x96(int(0.9 * WAD)),
        to_x96(int(0.95 * WAD)),
        to_x96(-WAD // 2),
    ]

    gas_data = []
    for x in erfinv_r1_inputs:
        gaussian.erfinv(x)
        gas_data.append(gaussian._computation.get_gas_used())
    results['erfinv_r1'] = {
        'min': min(gas_data),
        'max': max(gas_data),
        'avg': int(statistics.mean(gas_data)),
        'median': int(statistics.median(gas_data)),
    }

    # erfinv range 2
    erfinv_r2_inputs = [
        to_x96(int(0.97 * WAD)),
        to_x96(int(0.98 * WAD)),
        to_x96(int(-0.97 * WAD)),
        to_x96(int(-0.98 * WAD)),
    ]

    gas_data = []
    for x in erfinv_r2_inputs:
        gaussian.erfinv(x)
        gas_data.append(gaussian._computation.get_gas_used())
    results['erfinv_r2'] = {
        'min': min(gas_data),
        'max': max(gas_data),
        'avg': int(statistics.mean(gas_data)),
        'median': int(statistics.median(gas_data)),
    }

    # erfinv range 3
    erfinv_r3_inputs = [
        to_x96(int(0.99 * WAD)),
        to_x96(int(0.995 * WAD)),
        to_x96(int(0.999 * WAD)),
        to_x96(int(0.9999 * WAD)),
        to_x96(int(-0.99 * WAD)),
    ]

    gas_data = []
    for x in erfinv_r3_inputs:
        gaussian.erfinv(x)
        gas_data.append(gaussian._computation.get_gas_used())
    results['erfinv_r3'] = {
        'min': min(gas_data),
        'max': max(gas_data),
        'avg': int(statistics.mean(gas_data)),
        'median': int(statistics.median(gas_data)),
    }

    # erfinv all ranges
    erfinv_all_inputs = erfinv_r1_inputs + erfinv_r2_inputs + erfinv_r3_inputs

    gas_data = []
    for x in erfinv_all_inputs:
        gaussian.erfinv(x)
        gas_data.append(gaussian._computation.get_gas_used())
    results['erfinv_all'] = {
        'min': min(gas_data),
        'max': max(gas_data),
        'avg': int(statistics.mean(gas_data)),
        'median': int(statistics.median(gas_data)),
    }

    # erfcinv
    erfcinv_inputs = [
        WAD,
        WAD + WAD // 10,
        WAD // 2,
        3 * WAD // 2,
        int(0.01 * WAD),
        int(0.1 * WAD),
        int(1.9 * WAD),
    ]

    gas_data = []
    for x in erfcinv_inputs:
        gaussian.erfcinv(x)
        gas_data.append(gaussian._computation.get_gas_used())
    results['erfcinv'] = {
        'min': min(gas_data),
        'max': max(gas_data),
        'avg': int(statistics.mean(gas_data)),
        'median': int(statistics.median(gas_data)),
    }

    # cdf
    cdf_inputs = [
        (0, 0, WAD),
        (WAD, 0, WAD),
        (-WAD, 0, WAD),
        (2 * WAD, WAD, WAD),
        (0, -WAD, 2 * WAD),
        (3 * WAD, 0, WAD),
        (-3 * WAD, 0, WAD),
    ]

    gas_data = []
    for x, u, o in cdf_inputs:
        gaussian.cdf(x, u, o)
        gas_data.append(gaussian._computation.get_gas_used())
    results['cdf'] = {
        'min': min(gas_data),
        'max': max(gas_data),
        'avg': int(statistics.mean(gas_data)),
        'median': int(statistics.median(gas_data)),
    }

    # ppf
    ppf_inputs = [
        (WAD // 4, 0, WAD),
        (WAD // 2, 0, WAD),
        (3 * WAD // 4, 0, WAD),
        (int(0.1 * WAD), 0, WAD),
        (int(0.9 * WAD), 0, WAD),
        (int(0.01 * WAD), 0, WAD),
        (int(0.99 * WAD), 0, WAD),
    ]

    gas_data = []
    for x, u, o in ppf_inputs:
        gaussian.ppf(x, u, o)
        gas_data.append(gaussian._computation.get_gas_used())
    results['ppf'] = {
        'min': min(gas_data),
        'max': max(gas_data),
        'avg': int(statistics.mean(gas_data)),
        'median': int(statistics.median(gas_data)),
    }

    return results


def print_results(label: str, results: dict) -> None:
    """Print benchmark results in table format."""
    print(f"\n{label}")
    print("=" * 80)

    # Print individual results
    for func in ['erfc', 'erfinv_r1', 'erfinv_r2', 'erfinv_r3', 'erfinv_all', 'erfcinv', 'cdf', 'ppf']:
        if func not in results:
            continue
        stats = results[func]
        print(f"\n{func}:")
        print(f"  min: {stats['min']:6}, max: {stats['max']:6}, avg: {stats['avg']:6}, median: {stats['median']:6}")


def print_comparison(standard: dict, venom: dict) -> None:
    """Print side-by-side comparison with Solidity baseline."""
    print("\n" + "=" * 90)
    print("COMPARISON (pure computation = total - 118 gas call overhead)")
    print("=" * 90)
    print()

    print("| Function  | Solidity | Std Pure | Std vs Sol | Venom Pure | Venom vs Sol |")
    print("|-----------|----------|----------|------------|------------|--------------|")

    for func in ['erfc', 'erfcinv', 'cdf', 'ppf']:
        if func not in standard or func not in venom:
            continue

        sol = SOLGAUSS_BASELINE.get(func)
        if sol is None:
            continue

        std_pure = standard[func]['avg'] - CALL_OVERHEAD
        venom_pure = venom[func]['avg'] - CALL_OVERHEAD

        std_vs_sol = (std_pure - sol) / sol * 100
        venom_vs_sol = (venom_pure - sol) / sol * 100

        std_vs_str = f"{std_vs_sol:+.0f}%"
        venom_vs_str = f"{venom_vs_sol:+.0f}%"

        print(f"| {func:9} | {sol:8} | {std_pure:8} | {std_vs_str:>10} | {venom_pure:10} | {venom_vs_str:>12} |")


def main():
    print("\nvygauss Gas Benchmarks - Vyper 0.4.3+")
    print("=" * 80)

    print("\nBenchmarking with STANDARD compiler...")
    standard_results = benchmark_gaussian(experimental_codegen=False)
    print_results("STANDARD COMPILER RESULTS", standard_results)

    print("\n\nBenchmarking with VENOM compiler (--experimental-codegen)...")
    venom_results = benchmark_gaussian(experimental_codegen=True)
    print_results("VENOM COMPILER RESULTS", venom_results)

    # Print comparison
    print_comparison(standard_results, venom_results)

    print("\n" + "=" * 90)
    print("NOTES")
    print("=" * 90)
    print(f"""
Call overhead: {CALL_OVERHEAD} gas (subtract from titanoboa results for pure computation)
Venom: --experimental-codegen or compiler_args={{'experimental_codegen': True}}
Solidity baseline from solgauss README
""")


if __name__ == "__main__":
    main()
