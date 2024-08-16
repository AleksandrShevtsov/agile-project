# В этом файле необходимо создать функции:
# ● Функция на проверку валидных расширений файла
# ● Функция на проверку размерности файла (файл не должен быть больше 2 MB)
# ● Функция на создание пути для сохранения файла
# ● Функция на сохранение файла (файл должен записываться по частям для избежания
# потенциальных ошибок и потери данных)
import os
from pathlib import Path

ALLOWED_EXTENSIONS = ['.csv', '.doc', '.pdf', '.xlsx', '.py']


def check_extension(file_name):
    return Path(file_name).suffix in ALLOWED_EXTENSIONS


def check_file_size(file, required_size=2):
    file_size = file.size / (1024 * 1024)
    if file_size > required_size:
        return False
    return True


def create_file_path(file_name):
    new_file_name, file_ext = file_name.split('.')

    file_path = "documents/{}.{}".format(
        new_file_name,
        file_ext
    )

    return file_path


def save_file(file_path, file_content):
    os.makedirs(os.path.dirname('documents/'), exist_ok=True)

    with open(file_path, 'wb') as f:
        for chunk in file_content.chunks():
            f.write(chunk)

    return file_path

