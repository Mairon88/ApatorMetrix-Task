from typing import Union

from constants import PATH_TO_SO_FILE
from services import IPv4Tester
import sys

"""
Plik do uruchamiania metody delete jako subprocess
"""


def run_subprocess_delete(params: str) -> Union[str, None]:
    ipv4 = IPv4Tester(path=PATH_TO_SO_FILE)
    ipv4.lib_init()
    if "base_ip" in params:
        ipv4.add(params)
    del_result = ipv4.delete(params)
    if "ip_addr_to_check" in params:
        return ipv4.check(params)
    return del_result


if __name__ == "__main__":
    result = run_subprocess_delete(sys.argv[1])
    print(result)
