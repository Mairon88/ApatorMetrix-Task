import json
import os
import pytest
import subprocess
from constants import TWO_ARGUMENTS_0_GIVEN, TWO_ARGUMENTS_1_GIVEN, ARGUMENT_1_WRONG_TYPE, ARGUMENT_2_WRONG_TYPE, \
    FAILURE_CODE, SUCCESS_CODE, PATH_TO_SUB_ADD_FILE, PYTHON_VER
from services import ParamConverter


def run_subprocess_add(params):
    json_data = json.dumps(params)
    result = subprocess.run(
        [PYTHON_VER, PATH_TO_SUB_ADD_FILE, json_data],
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": os.path.abspath(os.getcwd())}
    )
    return result


@pytest.mark.parametrize("base_ip, mask", (("", ""), (None, None)))
def test_add_without_base_ip_and_mask(base_ip, mask):
    params = {"base_ip": base_ip, "mask": mask}
    result = run_subprocess_add(params)
    if result.returncode:
        assert f"Process finished with exit code {result.returncode}" == TWO_ARGUMENTS_0_GIVEN
    assert result.stdout.rstrip("\n") == TWO_ARGUMENTS_0_GIVEN


@pytest.mark.parametrize("mask", ("", None))
def test_add_without_mask(mask):
    base_ip = ParamConverter.convert_ip_to_int("10.20.0.0")
    params = {"base_ip": base_ip, "mask": mask}
    result = run_subprocess_add(params)
    if result.returncode:
        assert f"Process finished with exit code {result.returncode}" == TWO_ARGUMENTS_1_GIVEN
    assert result.stdout.rstrip("\n") == TWO_ARGUMENTS_1_GIVEN


@pytest.mark.parametrize("base_ip", ("", None))
def test_add_without_base_ip(base_ip):
    params = {"base_ip": base_ip, "mask": 16}
    result = run_subprocess_add(params)
    if result.returncode:
        assert f"Process finished with exit code {result.returncode}" == TWO_ARGUMENTS_1_GIVEN
    assert result.stdout.rstrip("\n") == TWO_ARGUMENTS_1_GIVEN


@pytest.mark.parametrize("base_ip", ["4294967296"])
def test_add_with_incorrect_type_base_ip(base_ip):
    params = {"base_ip": base_ip, "mask": 16}
    result = run_subprocess_add(params)
    if result.returncode:
        assert f"Process finished with exit code {result.returncode}" == ARGUMENT_1_WRONG_TYPE
    assert result.stdout.rstrip("\n") == ARGUMENT_1_WRONG_TYPE


@pytest.mark.parametrize("mask", ["16", 1000])
def test_add_with_incorrect_type_mask(mask):
    base_ip = ParamConverter.convert_ip_to_int("10.20.0.0")
    params = {"base_ip": base_ip, "mask": mask}
    result = run_subprocess_add(params)
    if result.returncode:
        assert f"Process finished with exit code {result.returncode}" == ARGUMENT_2_WRONG_TYPE
    assert result.stdout.rstrip("\n") == ARGUMENT_2_WRONG_TYPE


@pytest.mark.parametrize("base_ip, mask", ((9999999999, 16), (-1, 16)))
def test_add_with_incorrect_value_base_ip(base_ip, mask):
    params = {"base_ip": base_ip, "mask": mask}
    result = run_subprocess_add(params)
    if result.returncode:
        assert f"Process finished with exit code {result.returncode}" == FAILURE_CODE
    assert result.stdout.rstrip("\n") == FAILURE_CODE


@pytest.mark.parametrize("base_ip, mask", (("10.20.0.0", 55), ("10.20.0.0", 100), ("10.20.0.0", 255)))
def test_add_with_incorrect_value_mask(base_ip, mask):
    base_ip = ParamConverter.convert_ip_to_int(base_ip)
    params = {"base_ip": base_ip, "mask": mask}
    result = run_subprocess_add(params)
    if result.returncode:
        assert f"Process finished with exit code {result.returncode}" == FAILURE_CODE
    assert result.stdout.rstrip("\n") == FAILURE_CODE


@pytest.mark.parametrize("base_ip, mask",
                         (("10.20.0.0", 16), ("10.20.0.0", 24), ("10.20.0.0", 8), ("10.20.0.0", 12), ("10.20.0.0", 5)))
def test_add_with_correct_prefix(base_ip, mask):
    base_ip = ParamConverter.convert_ip_to_int(base_ip)
    params = {"base_ip": base_ip, "mask": mask}
    result = run_subprocess_add(params)
    if result.returncode:
        assert f"Process finished with exit code {result.returncode}" == SUCCESS_CODE
    assert result.stdout.rstrip("\n") == SUCCESS_CODE


def test_add_more_than_64_prefix():
    multi_prefix = [(ParamConverter.convert_ip_to_int(f"10.20.0.{fourth_octet}"), 16) for fourth_octet in range(80)]
    params = {"multi_prefix": multi_prefix}
    result = run_subprocess_add(params)
    if result.returncode:
        assert f"Process finished with exit code {result.returncode}" == FAILURE_CODE
    assert result.stdout.rstrip("\n") == FAILURE_CODE
