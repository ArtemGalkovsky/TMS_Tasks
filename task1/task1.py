"""
Есть папка, в которой лежат файлы с разными расширениями.
Программа должна:
● Вывести имя вашей ОС
● Вывести путь до папки, в которой вы находитесь
● Рассортировать файлы по расширениям, например, для
текстовых файлов создается папка, в неё перемещаются
все файлы с расширением .txt, то же самое для остальных
расширений
● После рассортировки выводится сообщение типа «в папке
с текстовыми файлами перемещено 5 файлов, их
суммарный размер - 50 гигабайт»
● Как минимум один файл в любой из получившихся
поддиректорий переименовать. Сделать вывод
сообщения типа «Файл data.txt был переименован в
some_data.txt»
● Программа должна быть кроссплатформенной – никаких
хардкодов с именем диска и слэшами.
"""
import errno
# WITHOUT FUNCTIONS AND CLASSES....

from os import name, getcwd, path, mkdir, listdir, rename
from sorted_move_back import move_back_files
from string import ascii_letters, digits
from random import randrange, choices
from shutil import rmtree, move

FILENAME_SYMBOLS = ascii_letters + digits + "_"

TRASH_RELATIVE_FOLDER_FROM_CURRENT = "trash"
SORTED_BY_EXTENSIONS_FOLDER_RELATIVE_PATH_FROM_CURRENT = "sorted"
NO_EXTENSION_FOLDER_FOR_SORTING = "NO_EXTENSION"

TRASH_PATH = path.join(getcwd(), TRASH_RELATIVE_FOLDER_FROM_CURRENT)
SORTED_BY_EXTENSIONS_FOLDER_PATH = path.join(getcwd(), SORTED_BY_EXTENSIONS_FOLDER_RELATIVE_PATH_FROM_CURRENT)


if __name__ == '__main__':
    sorted_files_result: dict = {}

    if not path.exists(TRASH_PATH):
        raise LookupError(f"{TRASH_PATH} does not exist...")


    if (path.exists(SORTED_BY_EXTENSIONS_FOLDER_PATH) and
            input("Move back files from sorted to trash? (y/n) > ").lower() == "y"):
        move_back_files(SORTED_BY_EXTENSIONS_FOLDER_PATH, TRASH_PATH)

    print("Type:", name)
    print("Path:", getcwd())

    if (path.exists(SORTED_BY_EXTENSIONS_FOLDER_PATH) and
            input(f"DO YOU WANT TO REMOVE FOLDER WITH FILES AT {SORTED_BY_EXTENSIONS_FOLDER_PATH}? (y/n) > ").lower() == "y"):
        print("Bye bye files...")
        rmtree(SORTED_BY_EXTENSIONS_FOLDER_PATH)

    if not path.exists(SORTED_BY_EXTENSIONS_FOLDER_PATH):
        mkdir(SORTED_BY_EXTENSIONS_FOLDER_PATH)

    for file in listdir(TRASH_PATH):
        current_file_path = path.join(TRASH_PATH, file)
        print(f"Sorting file: {file}={current_file_path}")

        dot_index = file.rfind(".")

        extension = NO_EXTENSION_FOLDER_FOR_SORTING
        if dot_index != -1:
            extension = file[dot_index + 1:].lower().strip()

        sorted_extension_path = path.join(SORTED_BY_EXTENSIONS_FOLDER_PATH, extension)
        if not path.exists(sorted_extension_path):
            print("Creating folder:", sorted_extension_path)
            mkdir(sorted_extension_path)

        sorted_file_path = path.join(sorted_extension_path, file)

        try:
            move(current_file_path, sorted_file_path)
            print("FILE SORTED!")

            if extension not in sorted_files_result:
                sorted_files_result[extension] = {"total_size": 0, "number_of_files": 0}

            sorted_files_result[extension]["total_size"] += path.getsize(sorted_file_path)
            sorted_files_result[extension]["number_of_files"] += 1

        except Exception as e:
            print("SOMETHING WENT WRONG WHEN SORTING:", e)


    for extension_folder in listdir(SORTED_BY_EXTENSIONS_FOLDER_PATH):
        path_to_extension_folder = path.join(SORTED_BY_EXTENSIONS_FOLDER_PATH, extension_folder)

        if path.isdir(path_to_extension_folder):
            files = listdir(path_to_extension_folder)

            to_rename_index = randrange(0, len(files))

            for index, file_with_extension in enumerate(files):

                file_with_extension_path = path.join(path_to_extension_folder, file_with_extension)
                if path.isfile(file_with_extension_path) and index == to_rename_index:
                    new_filename = "".join(
                        choices(FILENAME_SYMBOLS,
                                k=randrange(3, 16)
                                )
                    ) + "." + extension_folder

                    new_filename_path = path.join(path_to_extension_folder, new_filename)

                    try:
                        rename(file_with_extension_path, new_filename_path)
                        print(f"File in {extension_folder.upper()} {file_with_extension} has been renamed to {new_filename}")
                    except Exception as e:
                        print("SOMETHING WENT WRONG WHEN RENAMING:", e)


    print("STATS:")
    for extension, data in sorted_files_result.items():
        print(f"""{extension.upper()} results:
    Total size: {data['total_size']}bytes
    Files moved: {data['number_of_files']}""")