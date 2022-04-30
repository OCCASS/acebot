import logging


def load_bad_words():
    try:
        with open('../bad_words', 'r') as file:
            text = file.read().strip().replace(' ', '')

        return text.split(',')
    except (FileNotFoundError, FileExistsError):
        logging.error('File bad_words not found!')
        return []
