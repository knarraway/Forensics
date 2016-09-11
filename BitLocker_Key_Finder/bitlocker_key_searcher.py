## WIP ## 

import os
import collections
import re

SearchResult = collections.namedtuple('SearchResult', 'Identifier, Recovery_Key')


def main():
    folder = get_folder_from_user()
    if not folder:
        print("Sorry we can't search that location.")
        return

    text = get_search_text_from_user()
    checker_list = ['shallow', 'medium', 'deep', 'all']
    if not text:
        print("We can't search for nothing!")
        return
    if text not in checker_list:
        print("Unknown Entry! Please enter one of the listed inputs")
        return

    for file in file_finder(folder):
        if text == checker_list[0] or text == checker_list[3]:
            for m in shallow_search(file):
                print(m)
        if text == checker_list[1] or text == checker_list[3]:
            for m in medium_search(file):
                print(m)
        if text == checker_list[2] or text == checker_list[3]:
            deep_search(file)


def shallow_search(file):  # only opens files where the name contains 'BitLocker recovery', searches file for id and rk
    if 'BitLocker Recovery Key' in os.path.basename(file):  # lazy finder but fast - will find most keys
        with open(file, 'r', encoding='utf-16') as f:
            extracted_text = f.readlines()
            if 'Identifier:' in extracted_text[4]:
                identifier = extracted_text[6].strip()
                recovery_key = extracted_text[12].strip()
                key_combo = SearchResult(Identifier=identifier, Recovery_Key=recovery_key)
                yield key_combo


def medium_search(file):  # opens all files and searches the header for BitLocker drive encryption
    try:
        with open(file, 'r', encoding='utf-16') as f:  # reads top lines for all files, gets renamed files
            top_line = f.readline()
            if 'BitLocker Drive Encryption recovery key' in top_line:
                extracted_text = f.readlines()
                if 'Identifier:' in extracted_text[3]:
                    identifier = extracted_text[5].strip()
                    recovery_key = extracted_text[11].strip()
                    key_combo = SearchResult(Identifier=identifier, Recovery_Key=recovery_key)
                    yield key_combo
    except IOError as error:
        'Error Log: {}'.format(error)
    except UnicodeError:  # these are expected to happen, not all files will be UTF-16.
        pass


def deep_search(file):  # opens all files and regexes for just the rk format
    with open(file, 'rb') as f:
        text = f.read()
        r = re.findall(b'((?:\d{6}\-){7}\d{6})', text)
        print(r)
    # TODO search for just the recovery key format in regex
    # TODO ACCESS DENIED IN SOME FILES , TRY EXCEPT BLOCK


def get_folder_from_user():
    folder = input('What folder do you want to search? ')
    if not folder or not folder.strip():
        return None

    if not os.path.isdir(folder):
        return None

    return os.path.abspath(folder)


def get_search_text_from_user():
    text = input('What level of search? [shallow, medium, deep or all]')
    return text.lower()


def file_finder(file_path):
    for item in os.listdir(file_path):
        full_item = os.path.join(file_path, item)
        if os.path.isfile(full_item):
            yield full_item
        elif os.path.isdir(full_item):
            yield from file_finder(full_item)

if __name__ == '__main__':
    main()
