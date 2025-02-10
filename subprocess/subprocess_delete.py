from services import IPv4Lib
import sys


def run_subprocess_delete(prefix):
    ipv4 = IPv4Lib(path="c_files/IPv4.so")
    ipv4.lib_init()
    return ipv4.delete(prefix)

if __name__ == "__main__":
    prefix = sys.argv[1]
    result = run_subprocess_delete(prefix)
    print(result)