from services import IPv4Tester
import sys


def run_subprocess_check(ip_addr):
    ipv4 = IPv4Tester(path="c_files/IPv4.so")
    ipv4.lib_init()
    return ipv4.check(ip_addr)

if __name__ == "__main__":
    prefix = sys.argv[1]
    result = run_subprocess_check(prefix)
    print(result)