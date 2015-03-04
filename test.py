import sqlite3
import string
import code
import re
from bs4 import BeautifulSoup

errors = []


# Helper functions
def prepare():
    # Create database, table and index
    conn = sqlite3.connect("marathi.db")
    c = conn.cursor()
    create_string = '''
        CREATE TABLE IF NOT EXISTS marathi_words
        (
            letter string, word string, english_annotation string, data string
        )
    '''
    index_string_words = '''
        CREATE UNIQUE INDEX IF NOT EXISTS UniqueWords ON
        marathi_words (word)
    '''
    index_string_letters = '''
        CREATE INDEX IF NOT EXISTS IndexLetters ON
        marathi_words (letter)
    '''
    c.execute(create_string)
    c.execute(index_string_words)
    c.execute(index_string_letters)
    conn.commit()
    conn.close()


def __soupify(file_path, encoding='ISO-8859-1'):
    html_doc = open(file_path, 'r', encoding=encoding)
    return BeautifulSoup(html_doc)


def __push_array(insert_array):
    conn = sqlite3.connect("marathi.db")
    c = conn.cursor()
    try:
        execute_many_string = '''
            INSERT INTO marathi_words (letter, word, english_annotation, data)
            VALUES (?, ?, ?, ?)
        '''
        c.executemany(execute_many_string, insert_array)
    except sqlite3.OperationalError as e:
        errors.append([insert_array, 'push_array', e])
    finally:
        conn.commit()
        conn.close()


def parse_files(files):
    insert_array = []
    for file_path in files:
        insert_element = page_parser(file_path)
        insert_array.append(insert_element)
    __push_array(insert_array)


def page_parser(file_path):
    soup = __soupify(file_path)
    content_array = soup.select('p')
    print("Processing %s elements in %s" % (len(content_array), file_path))
    for content in content_array:
        def extract_letter(content):
            pass

        def extract_word(content):
            content.font.string

        def extract_english_annotation(content):
            re.search('\[(.*)\]', str(content)).group(1).strip()

        def extract_data(content):
            "rofl"

        try:
            code.interact(local=locals())
            letter = extract_letter(content)
            word = extract_word(content)
            english_annotation = extract_english_annotation(content)
            data = extract_data(content)

            return_list = (letter, word, english_annotation, data)
        except Exception as e:
            errors.append([letter, file_path, 'page_parser', e])
        return return_list


# Process
prepare()
file_paths = map(lambda letter: 'marathi_dict/%s.html' % letter,
                 string.ascii_lowercase)
parse_files(file_paths)

# Error reporting
print(errors)
