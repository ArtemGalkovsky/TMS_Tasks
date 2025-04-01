"""
7. Дан текстовый файл с несколькими строками.
Зашифровать шифром Цезаря, при этом шаг зависит от
номера строки: для первой строки шаг 1, для второй – 2 и т.д.
Пример:
Входные данные:
Hello
Hello
Hello
Hello
Выходные данные:
Ifmmp
Jgnnq
Khoor
Lipps
"""

from caesar import caesar_cipher_encode

text = \
"""Hello
Hello
Hello
Hello"""

for index, line in enumerate(text.splitlines(), 1):
    print(f"{line} -> {caesar_cipher_encode(line, index)} [key is {index}]")