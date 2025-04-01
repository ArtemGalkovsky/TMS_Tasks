"""
3. Напишите программу, которая считывает текст из
файла (в файле может быть больше одной строки) и выводит
в новый файл самое часто встречаемое слово в каждой
строке и число – счётчик количества повторений этого слова
в строке.
"""


from string import punctuation

with open("count.txt", "w+", encoding="utf-8") as fl:
    fl.write("")

with open("text.txt", "r", encoding="utf-8") as read_file, open("count.txt", "a+", encoding="utf-8") as write_file:
    for line in read_file:
        line = line.strip()

        if not line:
            write_file.write(f"  0\n")
            continue

        for punc in punctuation:
            line = line.replace(punc, "")

        print("Parsing line:", line)

        split_line_lowercase = tuple(map(str.lower, line.split()))
        no_repeated_line = set(split_line_lowercase)

        counts = {}
        for word in no_repeated_line:
            word_count = split_line_lowercase.count(word)
            counts[word] = word_count

        print("RESULT DICT:", counts)
        most_common_word = max(counts, key=counts.get)
        print(f"MOST COMMON WORD IS {most_common_word}, IT APPEARS {counts[most_common_word]} times!")

        write_file.write(f"{most_common_word} {counts[most_common_word]}\n")