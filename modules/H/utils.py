import unicodedata
import re
import os

from datetime import datetime
from docx import Document

from database import db_utils


def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


def get_article_filename(title):
    return slugify(title) + '.docx'


def get_article_filepath(title, score):
    filename = get_article_filename(title)
    script_path = os.path.dirname(os.path.realpath(__file__))
    emotion = 'negative' if score < 0 else 'positive'
    return os.path.join(script_path, '..', '..', 'Texts as found input', emotion, filename)

def save_article_file(article, score):
    document = Document()
    document.add_heading(article.title, 0)
    document.add_paragraph(article.text)
    filepath = get_article_filepath(article.title, score)
    document.save(filepath)

def save_search_to_db(query, query_type, articles, scores, from_date=None, until_date=None):
    with db_utils.db_connect() as conn:
        cursor = conn.cursor()
        result = cursor.execute("""
            INSERT INTO searches
            (timestamp, type, query, status, from_date, until_date)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (datetime.now(), query_type, query, 'started', from_date, until_date))

        search_id = result.lastrowid
        conn.commit()

        data = [(
                    a.title,
                    a.url,
                    a.publish_date,
                    get_article_filename(a.title),
                    search_id,
                    scores[a.url]
                ) for a in articles]

        cursor.executemany("""
            INSERT INTO documents
            (title, url, publish_date, filename, search_id, vader_score)
            VALUES (?, ?, ?, ?, ?, ?)""",
            data)
        conn.commit()

