import csv
import re

class CsvReader(object):
    words = []

    def __init__(self, filename):
        word_reader = csv.reader(open(filename, newline='', encoding='UTF-8'), delimiter=',')
        self.words = [row[1].lower() for row in word_reader]

    def get_words_as_list(self):
        return self.words