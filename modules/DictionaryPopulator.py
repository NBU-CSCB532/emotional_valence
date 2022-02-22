import os

import pandas as pd

from database import db_utils


class DictionaryPopulator():
    my_path = os.path.abspath(os.path.dirname(__file__))
    def populate(self):
        dictionary_path = os.path.abspath(
            os.path.join(self.my_path, '../', 'Dictionary', 'DICTIONARY Wordforms Transciptions.xlsx'))
        stop_words_path = os.path.abspath(
            os.path.join(self.my_path, '../', 'Dictionary', 'Dictionary Stop Words.xlsx'))

        correlation_path =os.path.abspath(
            os.path.join(self.my_path, 'Correlation.xlsx'))

        df = pd.read_excel(dictionary_path)
        df_stop_words = pd.read_excel(stop_words_path)
        df_correlation = pd.read_excel(correlation_path)
        conn = db_utils.db_connect()
        cur = conn.cursor()

        sql = 'DROP TABLE IF EXISTS dictionary'
        cur.execute(sql)

        sql = 'DROP TABLE IF EXISTS stop_words'
        cur.execute(sql)

        sql = 'DROP TABLE IF EXISTS syllables_weights'
        cur.execute(sql)

        conn.commit()

        df.to_sql('dictionary', con=conn, index=False)
        df_stop_words.to_sql('stop_words', con=conn, index=False)
        df_correlation.to_sql('syllables_weights', con=conn, index=False)
        conn.commit()

        sql = 'CREATE UNIQUE INDEX IF NOT EXISTS dictionary_word_lower_idx ON dictionary(lower(WordForm))'
        cur.execute(sql)

        sql = 'CREATE INDEX IF NOT EXISTS stop_words_word_lower_idx ON stop_words(lower(" Stop Words"))'
        cur.execute(sql)

        sql = 'CREATE UNIQUE INDEX IF NOT EXISTS syllables_weights_word_lower_idx ON syllables_weights(lower("Syllable_Key"))'
        cur.execute(sql)

        conn.commit()
        conn.close()

        print("Population of dictionaries finished")
