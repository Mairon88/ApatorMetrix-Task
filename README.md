# ApatorMetrix-Task 

## (link do wygenerowanego raportu z przeprowadzonych testów: https://mairon88.github.io/ApatorMetrix-Task/raport.html?sort=result)

### Treść Zadania 
Zaimplementowano bibliotekę dynamiczną (https://github.com/apator-metrix/InterviewKit), która zarządza zbiorem maksymalnie 64 prefiksów IPv4.

Prefiks określa zakres adresów wyrażony za pomocą wartości bazowej oraz maski, przy czym maska posiada ustawione tylko najbardziej znaczące bity w ilości wyrażonej dla uproszczenia liczbą.

Dla przykładu prefiks 10.20.0.0/16 oznacza zakres adresów 10.20.0.0 - 10.20.255.255, a prefiks 32.64.128.0/20 oznacza zakres 32.64.128.0 - 32.64.143.255.

Struktura danych przechowuje zbiór prefiksów czyli par - baza IP (32 bity) i maska (wartości 0 - 32).

Zostały zaimplementowane następujące funkcje:

int add(unsigned int base, char mask) - dodanie prefiksu do zbioru. Zwraca 0 lub -1 dla błędnych argumentów wywołania.

int del(unsigned int base, char mask) - usunięcie prefiksu ze zbioru. Zwraca 0 lub -1 dla błędnych argumentów wywołania.

char check(unsigned int ip) - sprawdzenie czy adres IP zawiera się w zbiorze prefiksów. Zwraca maskę najmniejszego prefiksu (o największej wartości maski) w zbiorze, który zawiera wskazany adres. Jeżeli IP nie zawiera się w zbiorze prefiksów zwraca -1.

 

Proszę napisać skrypt w Pythonie wywołujący program napisany w C. Skrypt powinien kompleksowo testować opisane wyżej funkcjonalności. Należy przewidzieć rozszerzanie przypadków testowych o nowe scenariusze.

Skrypt powinien generować raport z przeprowadzonych testów.

### Konfiguracja i uruchamianie skryptu

#### Tworzenie wirtualnego środowiska (.venv)
Linux:
        
        python3 -m venv .venv
        source .venv/bin/activate


Windows

        python -m venv .venv
        .\.venv\Scripts\Activate

#### Instalowanie paczek

        pip install -r requirements.txt


### Opis przygotowanego projektu do testowania biblioteki dynamicznej

Do przetestowania dynamicznej biblioteki IPv4.so wykorzystano bibliotekę <b>ctypes</b> z funkcją <b>CDLL</b> która pozwala na załadowanie i interakcję z bibliotekami dynamicznymi.
Dla łatwiejszej pracy z testowaną biblioteką przygotowano klasy CLibLoader (klasa bazowa) oraz IPv4Tester.
Klasa CLibLoader odpowiada za załadowanie biblioteki dynamicznej, a klasa IPv4Tester przygotowana została do przetestowania funkcjonalności biblioteki.

Do wykonania testów wykorzystano bibliotekę <b>pytest</b>, a do generowania raportu z przeprowadzonych testów wykorzystano <b>pytest-html</b>.

Zauważono, że występują nieoczekiwane błędy w dynamicznej bibliotecę, z tego względu testowane funkcje są uruchamiane jako osobne procesy, aby przechwytywać informacje m.in takie jak "Process finished with exit code 1" bez kończenia programu.
W związku z tym przygotowano pomocnicze pliki subprocess_add.py, subprocess_check.py oraz subprocess_delete.py, które są uruchamianę jako osobny proces i wywołuję testowane metody.

W plikach: test_add.py, test_check.py oraz test_delete.py znajdują się właściwe testy napisane z użyciem biblioteki <b>pytest</b>.

Przykładowy raport wygenerowany przez pytest-html znajduje się tutaj: [Link do raportu](https://mairon88.github.io/ApatorMetrix-Task/raport.html?sort=result)

### Wyniki przeprowadzonych testów

Skrypt wykonał 48 testów.

<span style="color:red;">21</span> testów zakończyło się niepowodzeniem.

<span style="color:green;">27 </span> testów zakończyło się sukcesem.


#### Po analizie negatywnych wyników testów można stwierdzić, że:
- #### Funkcja add:
    
    -  może przyjmować ip w postaci int, które wykracza poza zakres 0.0.0.0 - 255.255.255.255
    -  może przyjmować maskę, która wykracza poza zakres 0-32
    -  niektóre wartości maski powodują, że prefix nie zostaje przyjęty, np. ip 10.20.0.0 z maską 8, 16, 24 zostaje przyję, ale z maską 5 i 12 już nie.
    -  można dodać więcej niż 64 prefixy

- #### Funkcja check:
    
    -  w przypadku, kiedy funkcja check nie znajduje adresu ip, zwraca 255 zamiast -1
    -  dla prefixów np. 10.20.0.0/8 i 10.20.0.0/16 otrzymujemy wartość 255

- #### Funkcja delete:
    
    -  w niektórych przypadkach usuwania dodanego wcześniej prefixu można otrzymać "Process finished with exit code 1"
    -  usuwając prefix 10.20.0.0/24, który wcześniej nie został dodany, otrzymujemy 0 zamiast -1, to samo dla masek 16 i 32
