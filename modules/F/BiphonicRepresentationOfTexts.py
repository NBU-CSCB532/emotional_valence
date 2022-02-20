import os
import re
import pandas as pd

from database import db_utils


class BiphonicRepresentationOfTexts():
    def start(self):
        conn = db_utils.db_connect()
        conn.create_function('regexp', 2, lambda x, y: 1 if re.search(x, y) else 0)

        cur = conn.cursor()

        step_1_query = """
        select w.'news ID' || ' ' || w.'contains sentence ID' as Sentence,
        w.word as Word,
        w.position as Position,
        iif(lower(w.word) = 'the' and (select ww.word from words ww where ww.'news ID' = w.'news ID' and ww.'contains sentence ID' = w.'contains sentence ID' and ww.position = w.position + 1 and lower(ww.word) REGEXP '^[aeiouy]') is not null, w.word, iif(lower(w.word) = 'the', 'the''', w.word)) as WordTheDii,
        iif(lower(w.word) = 'the' and (select ww.word from words ww where ww.'news ID' = w.'news ID' and ww.'contains sentence ID' = w.'contains sentence ID' and ww.position = w.position + 1 and lower(ww.word) REGEXP '^[aeiouy]') is not null, ifnull(sw.'is a stop word', d.TranscriptAsFound), iif(lower(w.word) = 'the', '''ðə', ifnull(sw.'is a stop word', d.TranscriptAsFound))) as TranscriptOrStop,
        ifnull(sw.comment, (select ws.TranscriptSyl from words_syllables ws where lower(ws.WordForm) = lower(w.word) limit 1)) as TranscriptSyl
        from words w
        left join dictionary d on lower(d.WordForm) = lower(w.word)
        left join stop_words sw on lower(sw.' Stop Words') = lower(w.word)
        """

        cur.execute(step_1_query)
        step_1_result = cur.fetchall()

        print("Step 1 Done")

        step_2_query = """
        select w.'news ID' as filename,
        w.'news ID' || ' ' || w.'contains sentence ID' as Sentence,
        cast(substr(w.'contains sentence ID', 2, length(w.'contains sentence ID')) as integer) as NumberSentence,
        iif(lower(w.word) = 'the' and (select ww.word from words ww where ww.'news ID' = w.'news ID' and ww.'contains sentence ID' = w.'contains sentence ID' and ww.position = w.position + 1 and lower(ww.word) REGEXP '^[aeiouy]') is not null, w.word, iif(lower(w.word) = 'the', 'the''', w.word)) as Word,
        w.position as Position,
        iif(lower(w.word) = 'the' and (select ww.word from words ww where ww.'news ID' = w.'news ID' and ww.'contains sentence ID' = w.'contains sentence ID' and ww.position = w.position + 1 and lower(ww.word) REGEXP '^[aeiouy]') is not null, ifnull(sw.'is a stop word', d.TranscriptAsFound), iif(lower(w.word) = 'the', '''ðə', ifnull(sw.'is a stop word', d.TranscriptAsFound))) as TranscriptOrStop,
        ifnull(sw.comment, ws.TranscriptSyl) as TranscriptSyl,
        ws.Sequence as Sequence,
        ws.Syllable as Syllable,
        ws.SyllableKey as SyllableKey,
        ws.biphoneN as BiphoneN
        from words w
        left join dictionary d on lower(d.WordForm) = lower(w.word)
        left join stop_words sw on lower(sw.' Stop Words') = lower(w.word)
        left join words_syllables ws on lower(ws.WordForm) = lower(w.word)
        """

        drop_view = "drop view if exists final_biphone"
        cur.execute(drop_view)

        create_view = 'create view final_biphone as ' + step_2_query
        cur.execute(create_view)

        print("Step 2 Done")

        cur.execute('select distinct * from final_biphone order by sentence asc, position asc, sequence asc')
        step_2_result = cur.fetchall()
        cur.close()

        my_path = os.path.abspath(os.path.dirname(__file__))
        step_1_path = os.path.abspath(os.path.join(my_path, 'Biphone Step 1.csv'))
        step_2_path = os.path.abspath(os.path.join(my_path, 'Biphone Step 2.csv'))
        pd.DataFrame(step_1_result).to_csv(step_1_path,
                                             header=['Sentence', 'Word', 'Position', 'WordTheDii', 'TranscriptOrStop',
                                                     'TranscriptSyl'], index=False)
        pd.DataFrame(step_2_result).to_csv(step_2_path,
                                             header=['Filename', 'Sentence', 'NumberSentence', 'Word', 'Position',
                                                     'TranscriptOrStop', 'TranscriptSyl', 'Sequence', 'Syllable',
                                                     'SyllableKey', 'BiphoneN'], index=False)

        print("Populated biphonic representation of texts")
