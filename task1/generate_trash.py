from random import randrange, choices, choice
from string import ascii_letters, digits
from os import getcwd, path, mkdir

CURRENT_DIR = getcwd()
TRASH_FOLDER_RELATIVE_PATH_FROM_CURRENT = "trash"
EXTENSIONS = [".txt", ".jpg", ".jpeg", ".png", ".gif", ".docx", ".pdf", ".doc", ".mp3", ".mp4"]
FILENAME_SYMBOLS = ascii_letters + digits + "_"

if input("Gen trash? (Y/n) > ").lower() == "y":
    trash_folder = path.join(CURRENT_DIR, TRASH_FOLDER_RELATIVE_PATH_FROM_CURRENT)

    if not path.exists(trash_folder):
        mkdir(trash_folder)

    for i in range(30):
        extension = choice(EXTENSIONS)
        filename = "".join(
            choices(FILENAME_SYMBOLS,
                    k=randrange(3, 16)
                    )
        ) + extension
        filename_path = path.join(trash_folder, filename)

        with open(filename_path, "w+") as file:
            file.write("".join(choices(FILENAME_SYMBOLS, k=randrange(23732, 237327))))

        print("GENERATED:", filename_path, "WITH SIZE:", path.getsize(filename_path))