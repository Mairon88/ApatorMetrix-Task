from services import IPv4Tester
import sys


def run_subprocess_delete(params):
    ipv4 = IPv4Tester(path="c_files/IPv4.so")
    ipv4.lib_init()
    if "base_ip" in params:
        ipv4.add(params)
    del_result = ipv4.delete(params)
    if "ip_addr_to_check" in params:
        return ipv4.check(params)
    return del_result

if __name__ == "__main__":
    params = sys.argv[1]
    result = run_subprocess_delete(params)
    print(result)