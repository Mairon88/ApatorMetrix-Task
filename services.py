import ctypes
import ipaddress
from typing import Union


class CLibLoader:

    def __init__(self, path):
        self.path = path
        self.lib = self._load_lib()

    def _load_lib(self) -> Union[ctypes.CDLL, None]:
        try:
            lib = ctypes.CDLL(self.path)
            return lib
        except OSError as e:
            print(f"Wystąpił błąd podczas ładowania biblioteki:", {e})
        except Exception as e:
            print(f"Wystąpił błąd", {e})

    def lib_init(self) -> None:
        try:
            self.lib.init()
        except Exception as e:
            print(f"Biblioteka nie została załadowana i nie można wykonać metody init", {e})

    def lib_clear(self) -> None:
        try:
            self.lib.clear()
        except Exception as e:
            print(f"Biblioteka nie została załadowana i nie można wykonać metody clear", {e})


class IPv4Lib(CLibLoader):

    def __init__(self, path):
        super().__init__(path)

        if self.lib:
            self._define_function_signature()

    def _define_function_signature(self) -> None:
        try:
            self.lib.init.argtypes = []
            self.lib.init.restype = None

            self.lib.add.argtypes = [ctypes.c_uint, ctypes.c_char]
            self.lib.add.restype = ctypes.c_int

            self.lib.delete = getattr(self.lib, "del")
            delattr(self.lib, "del")
            self.lib.delete.argtypes = [ctypes.c_uint, ctypes.c_char]
            self.lib.delete.restype = ctypes.c_int

            self.lib.check.argtypes = [ctypes.c_uint]
            self.lib.check.restype = ctypes.c_char

            self.lib.clear.argtypes = []
            self.lib.clear.restype = None
        except Exception as e:
            print("Nie udało się zdefiniować typów", e)

    def add(self, prefix: str) -> Union[str, None]:
        try:
            splitted_prefix = prefix.split("/")
            base_ip = IpToInt.convert_ip_to_int(splitted_prefix[0])
            mask = bytes([int(splitted_prefix[1])])
            result_add = self.lib.add(base_ip, mask)
            # print(f"Result of add: {result_add}")
            return result_add
        except Exception as e:
            print("Nie udało się dodać prefixu", e)


    def delete(self, prefix: str) -> Union[str, None]:
        try:
            splitted_prefix = prefix.split("/")
            base_ip = IpToInt.convert_ip_to_int(splitted_prefix[0])
            mask = bytes([int(splitted_prefix[1])])
            result_delete = self.lib.delete(base_ip, mask)
            # print(f"Result of delete: {result_delete}")
            return result_delete
        except Exception as e:
            print("Nie udało się usunąć prefixu", e)

    def check(self, ip_addr: str) -> Union[int, None]:
        try:
            converted_ip = IpToInt.convert_ip_to_int(ip_addr)
            result_check = self.lib.check(converted_ip)

            # print(f"Result of check: {int.from_bytes(result_check, byteorder='big')}")
            return int.from_bytes(result_check, byteorder='big')
        except Exception as e:
            print("Nie można było sprawdzić czy adres ip znajduję się w zbiorze", e)


class IpToInt:

    @staticmethod
    def convert_ip_to_int(base_ip_address: str) -> Union[int, None]:
        try:
            ip_int = int(ipaddress.IPv4Address(base_ip_address))
            return ip_int
        except Exception as e:
            print("Nie udało się przekonwertować adresu ip na liczbę int ", e)


