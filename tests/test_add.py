import json
import os

import subprocess
from services import ParamConverter


def run_subprocess_add(params):
    json_data = json.dumps(params)
    result = subprocess.run(
        ["python3", "subprocess/subprocess_add.py", json_data],
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": os.path.abspath(os.getcwd())}
    )
    return result


def test_add_without_base_ip_and_mask():
    params = {}
    result = run_subprocess_add(params)
    assert result.stdout.rstrip("\n") == "this function takes at least 2 arguments (0 given)"


def test_add_without_mask():
    base_ip = ParamConverter.convert_ip_to_int("10.20.0.0")
    params = {"base_ip": base_ip}
    result = run_subprocess_add(params)
    assert result.stdout.rstrip("\n") == "this function takes at least 2 arguments (1 given)"


def test_add_without_base_ip():
    params = {"mask": 16}
    result = run_subprocess_add(params)
    assert result.stdout.rstrip("\n") == "this function takes at least 2 arguments (1 given)"


# dodać rózne parametry
def test_add_with_incorrect_type_base_ip():
    params = {"base_ip": "10.20.0.0/10", "mask": 16}
    result = run_subprocess_add(params)
    assert result.stdout.rstrip("\n") == "argument 1: TypeError: wrong type"


# dodać rózne parametry
def test_add_with_incorrect_type__mask():
    base_ip = ParamConverter.convert_ip_to_int("10.20.0.0")
    params = {"base_ip": base_ip, "mask": "xyz"}
    result = run_subprocess_add(params)
    assert result.stdout.rstrip("\n") == "argument 2: TypeError: wrong type"


# rózne wartosci
def test_add_with_incorrect_value_base_ip():
    params = {"base_ip": 4294967296, "mask": 16}
    result = run_subprocess_add(params)
    assert result.stdout.rstrip("\n") == '-1'


# dodać rózne parametry
def test_add_with_incorrect_value_mask():
    base_ip = ParamConverter.convert_ip_to_int("10.20.0.0")
    params = {"base_ip": base_ip, "mask": 55}
    result = run_subprocess_add(params)
    assert result.stdout.rstrip("\n") == '-1'


# dodać rózne parametry
def test_add_with_correct_prefix():
    base_ip = ParamConverter.convert_ip_to_int("10.20.0.0")
    params = {"base_ip": base_ip, "mask": 16}
    result = run_subprocess_add(params)
    assert result.stdout.rstrip("\n") == '0'


def test_add_more_than_64_prefix():
    multi_prefix = []
    for fourth_octet in range(3):
        for mask in range(1, 32):
            multi_prefix.append((ParamConverter.convert_ip_to_int(f"10.20.0.{fourth_octet}"), mask))
    params = {"multi_prefix": multi_prefix}
    result = run_subprocess_add(params)
    assert result.stdout.rstrip("\n") == '-1'
