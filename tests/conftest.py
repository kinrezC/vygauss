import pytest
import subprocess
import json


@pytest.fixture(scope="session")
def compiled_contract():
    result = subprocess.run(
        ["vyper", "-f", "abi,bytecode", "src/gaussian.vy"],
        capture_output=True,
        text=True,
        cwd="/home/mat/workspace/gauss-lib/vygauss",
    )
    if result.returncode != 0:
        raise RuntimeError(f"Compilation failed: {result.stderr}")

    output = result.stdout.strip()
    abi_str, bytecode = output.split("\n")
    return {"abi": json.loads(abi_str), "bytecode": bytecode}


@pytest.fixture
def wad():
    return 10**18


@pytest.fixture
def pow96():
    return 2**96
