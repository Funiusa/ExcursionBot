import os
import re
import shutil
import secrets

import phonenumbers

import config


def phone_validation(phone) -> bool:
    phone = phone if phone[0] == "+" else "+" + phone
    try:
        phone = phonenumbers.parse(phone)
        return phonenumbers.is_valid_number(phone)
    except phonenumbers.NumberParseException:
        return False


def save_file_from_response(folder, file, filename) -> str:
    new_filename = str(secrets.token_hex(5)) + "_" + filename
    folder_path = os.path.join(config.STATIC_IMG, folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = os.path.join(folder_path, new_filename)
    with open(file_path, "wb") as new_file:
        shutil.copyfileobj(file, new_file)
    return file_path


def save_addition_files(folder: str, files: list) -> str:
    folder_path = os.path.join(config.STATIC_IMG, folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    print(f"\n\n{folder_path}\n\n")
    for file in files:
        file_path = os.path.join(folder_path, file.filename)
        with open(file_path, "wb") as new_file:
            shutil.copyfileobj(file.file, new_file)

    return folder_path


def get_addition_data(path: str) -> list:
    files = []
    if path and os.path.exists(path):
        for root, _, filenames in os.walk(path):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                files.append(file_path)
    return files


def clear_answer(line: str) -> str:
    answer = "".join(re.findall(r"\b\w+\b", line)).lower()
    return answer
