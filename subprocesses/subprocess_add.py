from typing import Union

from constants import PATH_TO_SO_FILE
from services import IPv4Tester
import sys

"""
Plik do uruchamiania metody add jako subprocess
"""


def run_subprocess_add(params: str) -> Union[str, None]:
    ipv4 = IPv4Tester(path=PATH_TO_SO_FILE)
    ipv4.lib_init()
    return ipv4.add(params)


if __name__ == "__main__":
    result = run_subprocess_add(sys.argv[1])
    print(result)
