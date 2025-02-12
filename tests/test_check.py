import json
import os

import pytest

import subprocess
from constants import FAILURE_CODE
from services import ParamConverter


def run_subprocess_check(params):
    json_data = json.dumps(params)
    result = subprocess.run(
        ["python3", "subprocess/subprocess_check.py", json_data],
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": os.path.abspath(os.getcwd())}
    )
    return result


@pytest.mark.parametrize("base_ip, mask, ip_addr_to_check", (
        ("10.20.0.0", 24, "10.20.0.0"), ("10.20.0.0", 24, "10.20.0.255"), ("10.20.0.0", 8, "10.20.0.20"),
        ("10.20.0.0", 16, "10.20.0.0")))
def test_check_correct_ip_in_added_prefix(base_ip, mask, ip_addr_to_check):
    base_ip = ParamConverter.convert_ip_to_int(base_ip)
    ip_addr_to_check = ParamConverter.convert_ip_to_int(ip_addr_to_check)
    params = {"base_ip": base_ip, "mask": mask, "ip_addr_to_check": ip_addr_to_check}
    result = run_subprocess_check(params)
    assert result.stdout.rstrip("\n") == str(mask)


@pytest.mark.parametrize("base_ip, mask, ip_addr_to_check", (
        ("10.20.0.0", 16, "10.21.0.0"), ("198.55.0.0", 24, "198.55.125.0"), ("254.254.0.0", 8, "250.1.12.0")))
def test_check_incorrect_ip_in_added_prefix(base_ip, mask, ip_addr_to_check):
    base_ip = ParamConverter.convert_ip_to_int(base_ip)
    ip_addr_to_check = ParamConverter.convert_ip_to_int(ip_addr_to_check)
    params = {"base_ip": base_ip, "mask": mask, "ip_addr_to_check": ip_addr_to_check}
    result = run_subprocess_check(params)
    assert result.stdout.rstrip("\n") == FAILURE_CODE


@pytest.mark.parametrize("multi_prefix, ip_addr_to_check, expected", (
        ([(ParamConverter.convert_ip_to_int("10.20.0.0"), 24), (ParamConverter.convert_ip_to_int("10.20.0.0"), 32)],
         "10.20.0.0", '32'),
        ([(ParamConverter.convert_ip_to_int("10.20.0.50"), 24), (ParamConverter.convert_ip_to_int("10.20.0.0"), 32)],
         "10.20.0.0", '32'),
        ([(ParamConverter.convert_ip_to_int("10.20.0.0"), 24), (ParamConverter.convert_ip_to_int("10.20.0.150"), 32)],
         "10.20.0.0", '24'),
))
def test_check_correct_ip_in_added_multi_prefix(multi_prefix, ip_addr_to_check, expected):
    ip_addr_to_check = ParamConverter.convert_ip_to_int(ip_addr_to_check)
    params = {"multi_prefix": multi_prefix, "ip_addr_to_check": ip_addr_to_check}
    result = run_subprocess_check(params)
    assert result.stdout.rstrip("\n") == expected
