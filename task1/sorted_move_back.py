from os import listdir, path
from shutil import move

def move_back_files(sorted_by_extensions_folder_path: str, trash_path: str) -> None:
    for extension_folder in listdir(sorted_by_extensions_folder_path):
        path_to_extension_folder = path.join(sorted_by_extensions_folder_path, extension_folder)

        if path.isdir(path_to_extension_folder):

            for file_with_extension in listdir(path_to_extension_folder):
                file_with_extension_path = path.join(path_to_extension_folder, file_with_extension)
                if path.isfile(file_with_extension_path):
                    move(file_with_extension_path, trash_path)

__all__ = ["move_back_files"]
