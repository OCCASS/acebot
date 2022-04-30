import logging


def load_bad_words():
    try:
        with open('bad_words', 'r', encoding='utf-8') as file:
            text = file.read().strip()

        return text.split(', ')
    except (FileNotFoundError, FileExistsError):
        logging.error('File bad_words not found!')
        return []
