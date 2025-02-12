import json
import os
import pytest
import subprocess
from constants import TWO_ARGUMENTS_0_GIVEN, TWO_ARGUMENTS_1_GIVEN, \
    FAILURE_CODE, SUCCESS_CODE, PATH_TO_SUB_DELETE_FILE, PYTHON_VER
from services import ParamConverter


def run_subprocess_delete(params):
    json_data = json.dumps(params)
    result = subprocess.run(
        [PYTHON_VER, PATH_TO_SUB_DELETE_FILE, json_data],
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": os.path.abspath(os.getcwd())}
    )
    return result


@pytest.mark.parametrize("base_ip, mask, base_ip_to_del, mask_to_del", (
        ("10.20.0.0", 16, "", ""), ("198.55.0.0", 24, None, None)))
def test_delete_without_base_ip_and_mask(base_ip, mask, base_ip_to_del, mask_to_del):
    base_ip = ParamConverter.convert_ip_to_int(base_ip)
    params = {"base_ip": base_ip, "mask": mask, "base_ip_to_del": base_ip_to_del, "mask_to_del": mask_to_del}
    result = run_subprocess_delete(params)
    if result.returncode:
        assert f"Process finished with exit code {result.returncode}" == TWO_ARGUMENTS_0_GIVEN
    assert result.stdout.rstrip("\n") == TWO_ARGUMENTS_0_GIVEN


@pytest.mark.parametrize("base_ip, mask, base_ip_to_del, mask_to_del", (
        ("10.20.0.0", 16, "10.20.0.0", ""), ("198.55.0.0", 24, "198.55.0.0", None)))
def test_delete_without_mask(base_ip, mask, base_ip_to_del, mask_to_del):
    base_ip = ParamConverter.convert_ip_to_int(base_ip)
    base_ip_to_del = ParamConverter.convert_ip_to_int(base_ip_to_del)
    params = {"base_ip": base_ip, "mask": mask, "base_ip_to_del": base_ip_to_del, "mask_to_del": mask_to_del}
    result = run_subprocess_delete(params)
    if result.returncode:
        assert f"Process finished with exit code {result.returncode}" == TWO_ARGUMENTS_1_GIVEN
    assert result.stdout.rstrip("\n") == TWO_ARGUMENTS_1_GIVEN


@pytest.mark.parametrize("base_ip, mask, base_ip_to_del, mask_to_del", (
        ("10.20.0.0", 16, "", 16), ("198.55.0.0", 24, None, 24)))
def test_delete_without_base_ip(base_ip, mask, base_ip_to_del, mask_to_del):
    base_ip = ParamConverter.convert_ip_to_int(base_ip)
    params = {"base_ip": base_ip, "mask": mask, "base_ip_to_del": base_ip_to_del, "mask_to_del": mask_to_del}
    result = run_subprocess_delete(params)
    if result.returncode:
        assert f"Process finished with exit code {result.returncode}" == TWO_ARGUMENTS_1_GIVEN
    assert result.stdout.rstrip("\n") == TWO_ARGUMENTS_1_GIVEN


@pytest.mark.parametrize("base_ip, mask", (
        ("10.20.0.0", 8), ("198.55.0.0", 16), ("10.20.0.0", 24), ("198.55.0.0", 32)))
def test_delete_with_correct_prefix_after_add_prefix(base_ip, mask):
    base_ip = ParamConverter.convert_ip_to_int(base_ip)
    base_ip_to_del = ParamConverter.convert_ip_to_int(base_ip)
    params = {"base_ip": base_ip, "mask": mask, "base_ip_to_del": base_ip_to_del, "mask_to_del": mask}
    result = run_subprocess_delete(params)
    if result.returncode:
        assert f"Process finished with exit code {result.returncode}" == SUCCESS_CODE
    assert result.stdout.rstrip("\n") == SUCCESS_CODE


@pytest.mark.parametrize("base_ip_to_del, mask_to_del", (
        ("10.20.0.0", 8), ("198.55.0.0", 16), ("10.20.0.0", 24), ("198.55.0.0", 32)))
def test_delete_with_correct_prefix_before_add_prefix(base_ip_to_del, mask_to_del):
    base_ip_to_del = ParamConverter.convert_ip_to_int(base_ip_to_del)
    params = {"base_ip_to_del": base_ip_to_del, "mask_to_del": mask_to_del}
    result = run_subprocess_delete(params)
    if result.returncode:
        assert f"Process finished with exit code {result.returncode}" == FAILURE_CODE
    assert result.stdout.rstrip("\n") == FAILURE_CODE


@pytest.mark.parametrize("base_ip, mask", (
        ("10.20.0.0", 8), ("198.55.0.0", 16), ("10.20.0.0", 24), ("198.55.0.0", 32)))
def test_check_deleted_prefix(base_ip, mask):
    base_ip = base_ip_to_del = ip_addr_to_check = ParamConverter.convert_ip_to_int(base_ip)
    params = {"base_ip": base_ip, "mask": mask, "base_ip_to_del": base_ip_to_del, "mask_to_del": mask,
              "ip_addr_to_check": ip_addr_to_check}
    result = run_subprocess_delete(params)
    if result.returncode:
        assert f"Process finished with exit code {result.returncode}" == FAILURE_CODE
    assert result.stdout.rstrip("\n") == FAILURE_CODE
