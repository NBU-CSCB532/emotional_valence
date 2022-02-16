import os
import shutil
from database import db_utils

BIPHONE_INPUT_XLSX = '../BiphoneInput/BiphoneInput.xlsx'
SKELETON_BIPHONE_INPUT_XLSX = '../Skeleton/BiphoneInput/BiphoneInput.xlsx'
DECOMPOSED_TEXTS_PATH = '../Decomposed Texts'
TEXTS_PATH = '../Texts'
TEXTS_AS_FOUND_INPUT_NEGATIVE = '../Texts as found input/negative'
TEXTS_AS_FOUND_INPUT_POSITIVE = '../Texts as found input/positive'
TEXTS_FILTERED_PROTECTED = '../TextsFiltered–protected'
STOP_WORDS = '../Stop words'
FINAL_PATH = 'G'
NOVEL_WORDS_TRANSCRIBED = '../Novel Word/Transcribed.xlsx'
NOVEL_WORDS_NONTRANSCRIBED = '../Novel Word/Nontranscribed.xlsx'
SKELETON_NOVEL_WORDS_TRANSCRIBED = '../Skeleton/Novel Word/Transcribed.xlsx'
SKELETON_NOVEL_WORDS_NONTRANSCRIBED = '../Skeleton/Novel Word/Nontranscribed.xlsx'
BIPHONE_STEP_1 = 'F/Biphone Step 1.xlsx'
SKELETON_BIPHONE_STEP_1 = '../Skeleton/modules/F/Biphone Step 1.xlsx'
BIPHONE_STEP_2 = 'F/Biphone Step 2.xlsx'
SKELETON_BIPHONE_STEP_2 = '../Skeleton/modules/F/Biphone Step 2.xlsx'
TMPSAMPLE = '../Texts as found input/tmpSample.xlsx'
SKELETON_TMPSAMPLE = '../Skeleton/Texts as found input/tmpSample.xlsx'
SAMPLE = '../Texts as found input/sample.xlsx'
SKELETON_SAMPLE = '../Skeleton/Texts as found input/sample.xlsx'


class ProjectCleaner():
    def clean(self):
        while True:
            data = input('Start cleaning? (Y) or (N)?')
            if data.lower() not in ('y', 'n'):
                print("Choose (Y) or (N)")
            else:
                if data.lower() == 'y':
                    self.replace(BIPHONE_INPUT_XLSX, SKELETON_BIPHONE_INPUT_XLSX)
                    self.cleanDirectory(TEXTS_PATH)
                    self.cleanDirectory(TEXTS_AS_FOUND_INPUT_NEGATIVE)
                    self.cleanDirectory(TEXTS_AS_FOUND_INPUT_POSITIVE)
                    self.cleanDirectory(TEXTS_FILTERED_PROTECTED)
                    self.cleanDirectory(STOP_WORDS)
                    self.cleanDirectory(DECOMPOSED_TEXTS_PATH)
                    self.cleanDirectory(FINAL_PATH)
                    self.replace(NOVEL_WORDS_TRANSCRIBED, SKELETON_NOVEL_WORDS_TRANSCRIBED)
                    self.replace(NOVEL_WORDS_NONTRANSCRIBED, SKELETON_NOVEL_WORDS_NONTRANSCRIBED)
                    self.replace(BIPHONE_STEP_1, SKELETON_BIPHONE_STEP_1)
                    self.replace(BIPHONE_STEP_2, SKELETON_BIPHONE_STEP_2)
                    self.replace(SAMPLE, SKELETON_SAMPLE)
                    self.replace(TMPSAMPLE, SKELETON_TMPSAMPLE)
                    self.dropTableIfExists('words')

                    while True:
                        data = input('Start the program(Y) or exit(N)? ')
                        if data.lower() not in ('y', 'n'):
                            print("Choose (Y) or (N)")
                        else:
                            if data.lower() == 'y':
                                break
                            elif data.lower() == 'n':
                                exit()

                elif data.lower() == 'n':
                    break


        pass

    def cleanDirectory(self, dir):
        print("Now cleaning " + self.toPath(dir))
        if os.path.exists(self.toPath(dir)):
            for file in os.listdir(self.toPath(dir)):
                if '.py' not in file and '__pycache__' not in file:
                    toRemove = self.toPath(dir + '/' + file)
                    print("Now removing: " + toRemove)
                    os.remove(toRemove)
        else:
            print(self.toPath(dir) + " not found!")

    def replace(self, toRemove, toReplace):
        print("Now replacing " + self.toPath(toRemove))
        if os.path.exists(self.toPath(toRemove)):
            toRemove = self.toPath(toRemove)
            print("Now removing: " + toRemove)
            os.remove(toRemove)
        else:
            print(self.toPath(toRemove) + " not found!")

        toReplace = self.toPath(toReplace)
        toRemove = self.toPath(toRemove)
        print("Now copying: " + toReplace)
        shutil.copy(toReplace, toRemove[0:toRemove.rindex('/')])

    def dropTableIfExists(self, table_name):
        conn = db_utils.db_connect()
        cur = conn.cursor()

        sql = 'DROP TABLE IF EXISTS ' + table_name
        print("EXECUTING SQL QUERY: " + sql)
        cur.execute(sql)
        conn.commit()

    def toPath(self, path):
        db_utils.db_connect()
        return os.path.join(os.path.dirname(__file__), path)
