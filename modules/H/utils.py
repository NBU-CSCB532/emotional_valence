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

        return search_id


def get_documents_for_search(search_id):
    with db_utils.db_connect() as conn:
        cursor = conn.cursor()
        return cursor.execute(
                'SELECT * FROM documents WHERE search_id = ?',
                (search_id,))


def update_document_biphone_score(document_id, score):
    with db_utils.db_connect() as conn:
        cursor = conn.cursor()
        result = cursor.execute(
                'UPDATE documents SET biphone_score = ? WHERE id = ?',
                (score, document_id))


def update_search_status(search_id, status):
    with db_utils.db_connect() as conn:
        cursor = conn.cursor()
        result = cursor.execute(
                'UPDATE searches SET status = ? WHERE id = ?',
                (status, search_id))


def get_searches():
    with db_utils.db_connect() as conn:
        cursor = conn.cursor()
        return cursor.execute(
                'SELECT * FROM searches ORDER BY timestamp DESC')


def get_search(id):
    with db_utils.db_connect() as conn:
        cursor = conn.cursor()
        return cursor.execute(
                'SELECT * FROM searches WHERE id = ?', (id,)).fetchone()


def read_document(title, score):
    filepath = get_article_filepath(title, score)
    doc = Document(filepath)
    paragraphs = []
    for paragraph in doc.paragraphs:
        if paragraph:
            paragraphs += [p for p in paragraph.text.split('\n') if p != '']
    return paragraphs
