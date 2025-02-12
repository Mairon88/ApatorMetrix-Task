from typing import Union

from constants import PATH_TO_SO_FILE
from services import IPv4Tester
import sys

"""
Plik do uruchamiania metody check jako subprocess
"""


def run_subprocess_check(params: str) -> Union[int, None]:
    ipv4 = IPv4Tester(path=PATH_TO_SO_FILE)
    ipv4.lib_init()
    ipv4.add(params)
    return ipv4.check(params)


if __name__ == "__main__":
    result = run_subprocess_check(sys.argv[1])
    print(result)
