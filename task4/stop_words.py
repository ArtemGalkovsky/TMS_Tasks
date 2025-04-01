"""
4. Напишите программу, которая получает на вход строку
с названием текстового файла и выводит на экран
содержимое этого файла, заменяя все запрещённые слова
звездочками. Запрещённые слова, разделённые символом
пробела, должны храниться в файле stop_words.txt.
Программа должна находить
запрещённые слова в любом месте файла, даже в середине
другого слова. Замена независима от регистра: если в списке
запрещённых есть слово exam, то замениться должны exam,
eXam, EXAm и другие вариации.
Пример: в stop_words.txt записаны слова: hello email
python the exam wor is
Текст файла для цензуры выглядит так: Hello, World! Python
IS the programming language of thE future. My EMAIL is...
PYTHON as AwESOME!
Тогда итоговый текст: *****, ***ld! ****** ** *** programming
language of *** future. My ***** **... ****** ** awesome!!!!
"""

from os import path, getcwd
from re import findall, IGNORECASE

STOP_WORDS_FILE = path.join(getcwd(), 'stop_words.txt')
DEFAULT_TEXT_FILE = path.join(getcwd(), 'text.txt')

text_file = input("Enter text file path or nothing to use default file > ")

path_to_file = text_file if text_file else DEFAULT_TEXT_FILE

with open(path_to_file, "r", encoding="utf-8") as fl:
    text = fl.read()

with open(STOP_WORDS_FILE, "r", encoding="utf-8") as fl:
    stop_words = fl.read().split()

for blocked_word in stop_words:
    print("Searching for:", blocked_word)
    for found in findall(blocked_word, text, IGNORECASE):
        print(f"Blocking {found}!")
        text = text.replace(found, "*" * len(found))

print("Result:")
print(text)