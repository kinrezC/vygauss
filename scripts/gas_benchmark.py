#!/usr/bin/env python3
import boa
from pathlib import Path
import statistics

WAD = 10**18
POW96 = 2**96


def to_x96(x_wad: int) -> int:
    return (x_wad << 96) // WAD


def main():
    contract_path = Path(__file__).parent.parent / "src" / "gaussian.vy"
    gaussian = boa.load(str(contract_path))

    print("vygauss Gas Benchmarks")
    print("=" * 60)

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

    print("\nerfc:")
    gas_data = []
    for x in erfc_inputs:
        gaussian.erfc(x)
        gas_data.append(gaussian._computation.get_gas_used())

    print(
        f"  min: {min(gas_data)}, max: {max(gas_data)}, avg: {int(statistics.mean(gas_data))}, median: {int(statistics.median(gas_data))}"
    )

    erfinv_r1_inputs = [
        to_x96(0),
        to_x96(WAD // 10),
        to_x96(WAD // 2),
        to_x96(int(0.9 * WAD)),
        to_x96(int(0.95 * WAD)),
        to_x96(-WAD // 2),
    ]

    print("\nerfinv (Range 1: 0-0.96):")
    gas_data = []
    for x in erfinv_r1_inputs:
        gaussian.erfinv(x)
        gas_data.append(gaussian._computation.get_gas_used())

    print(
        f"  min: {min(gas_data)}, max: {max(gas_data)}, avg: {int(statistics.mean(gas_data))}, median: {int(statistics.median(gas_data))}"
    )

    erfinv_r2_inputs = [
        to_x96(int(0.97 * WAD)),
        to_x96(int(0.98 * WAD)),
        to_x96(int(-0.97 * WAD)),
        to_x96(int(-0.98 * WAD)),
    ]

    print("\nerfinv (Range 2: 0.96-0.99):")
    gas_data = []
    for x in erfinv_r2_inputs:
        gaussian.erfinv(x)
        gas_data.append(gaussian._computation.get_gas_used())

    print(
        f"  min: {min(gas_data)}, max: {max(gas_data)}, avg: {int(statistics.mean(gas_data))}, median: {int(statistics.median(gas_data))}"
    )

    erfinv_r3_inputs = [
        to_x96(int(0.99 * WAD)),
        to_x96(int(0.995 * WAD)),
        to_x96(int(0.999 * WAD)),
        to_x96(int(0.9999 * WAD)),
        to_x96(int(-0.99 * WAD)),
    ]

    print("\nerfinv (Range 3: 0.99-1):")
    gas_data = []
    for x in erfinv_r3_inputs:
        gaussian.erfinv(x)
        gas_data.append(gaussian._computation.get_gas_used())

    print(
        f"  min: {min(gas_data)}, max: {max(gas_data)}, avg: {int(statistics.mean(gas_data))}, median: {int(statistics.median(gas_data))}"
    )

    erfinv_all_inputs = erfinv_r1_inputs + erfinv_r2_inputs + erfinv_r3_inputs

    print("\nerfinv (all ranges):")
    gas_data = []
    for x in erfinv_all_inputs:
        gaussian.erfinv(x)
        gas_data.append(gaussian._computation.get_gas_used())

    print(
        f"  min: {min(gas_data)}, max: {max(gas_data)}, avg: {int(statistics.mean(gas_data))}, median: {int(statistics.median(gas_data))}"
    )

    erfcinv_inputs = [
        WAD,
        WAD + WAD // 10,
        WAD // 2,
        3 * WAD // 2,
        int(0.01 * WAD),
        int(0.1 * WAD),
        int(1.9 * WAD),
    ]

    print("\nerfcinv:")
    gas_data = []
    for x in erfcinv_inputs:
        gaussian.erfcinv(x)
        gas_data.append(gaussian._computation.get_gas_used())

    print(
        f"  min: {min(gas_data)}, max: {max(gas_data)}, avg: {int(statistics.mean(gas_data))}, median: {int(statistics.median(gas_data))}"
    )

    cdf_inputs = [
        (0, 0, WAD),
        (WAD, 0, WAD),
        (-WAD, 0, WAD),
        (2 * WAD, WAD, WAD),
        (0, -WAD, 2 * WAD),
        (3 * WAD, 0, WAD),
        (-3 * WAD, 0, WAD),
    ]

    print("\ncdf:")
    gas_data = []
    for x, u, o in cdf_inputs:
        gaussian.cdf(x, u, o)
        gas_data.append(gaussian._computation.get_gas_used())

    print(
        f"  min: {min(gas_data)}, max: {max(gas_data)}, avg: {int(statistics.mean(gas_data))}, median: {int(statistics.median(gas_data))}"
    )

    ppf_inputs = [
        (WAD // 4, 0, WAD),
        (WAD // 2, 0, WAD),
        (3 * WAD // 4, 0, WAD),
        (int(0.1 * WAD), 0, WAD),
        (int(0.9 * WAD), 0, WAD),
        (int(0.01 * WAD), 0, WAD),
        (int(0.99 * WAD), 0, WAD),
    ]

    print("\nppf:")
    gas_data = []
    for x, u, o in ppf_inputs:
        gaussian.ppf(x, u, o)
        gas_data.append(gaussian._computation.get_gas_used())

    print(
        f"  min: {min(gas_data)}, max: {max(gas_data)}, avg: {int(statistics.mean(gas_data))}, median: {int(statistics.median(gas_data))}"
    )


if __name__ == "__main__":
    main()
