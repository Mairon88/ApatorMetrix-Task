from services import IPv4Tester
import sys


def run_subprocess_check(params):
    ipv4 = IPv4Tester(path="c_files/IPv4.so")
    ipv4.lib_init()
    ipv4.add(params)
    return ipv4.check(params)

if __name__ == "__main__":
    result = run_subprocess_check(sys.argv[1])
    print(result)
