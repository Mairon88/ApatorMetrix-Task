from services import IPv4Tester
import sys


def run_subprocess_add(params):
    ipv4 = IPv4Tester(path="c_files/IPv4.so")
    ipv4.lib_init()
    return ipv4.add(params)

if __name__ == "__main__":
    result = run_subprocess_add(sys.argv[1])
    print(result)
