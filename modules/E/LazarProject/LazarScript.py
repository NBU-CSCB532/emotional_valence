from modules.E.LazarProject.Modules.Utils import get_key_by_value
from modules.E.LazarProject.Readers import ExcelReader
from modules.E.LazarProject.Modules import SyllableFinder, ExcelGenerator
from modules.E.LazarProject.Modules import CsvGenerator
import collections
import os


class LazarScript:
    my_path = os.path.abspath(os.path.dirname(__file__))
    input_path = os.path.join(my_path, '../../../', 'BiphoneInput', 'BiphoneInput.xlsx')

    def start(self):

        my_excel_reader_dict = ExcelReader.ExcelReader(self.input_path)
        my_excel_reader = ExcelReader.ExcelReader(os.path.join(self.my_path, "Syllables.xlsx"))
        words_list = my_excel_reader_dict.get_words_as_list()
        original_wordform_mapping = my_excel_reader_dict.get_reverse_mapping()
        syllable_key_mapping = my_excel_reader.get_syllable_key_mapping()
        biphone_mapping = my_excel_reader.get_biphone_mapping()
        syllable_finder = SyllableFinder.SyllableFinder(words_list)
        mapping = syllable_finder.get_syllables_mapping()
        sounds_mapping = my_excel_reader.get_mapping()

        for word, syllables in mapping.items():
            # print(word, syllables))
            for i, elem in enumerate(mapping[word]):
                # print(syllables)
                # print(list(filter(lambda s: get_key_by_value(sounds_mapping, s), syllables)))
                mapping[word][i] = list(filter(lambda s: get_key_by_value(sounds_mapping, s), mapping[word][i]))
            # print(mapping[word])
            new_word = []

            for elem in mapping[word]:
                if len(elem) > 0:
                    max_elem = ''
                    for el in elem:
                        # print(el)
                        if len(el) > len(max_elem):
                            max_elem = el
                    new_word.append(max_elem)

            words_to_remove = []
            # print(new_word)

            for word_i in new_word:
                for other_word in new_word:
                    if word_i != other_word and word_i in other_word:
                        words_to_remove.append(word_i)
            # print(words_to_remove)
            for word_i in words_to_remove:
                if word_i in new_word:
                    new_word.remove(word_i)
            # print(mapping[word])
            # mapping[word] = [new_word]
            # print(type(mapping[word]))
            # if str(word) == str("'aɪbi:em"):
            #     print(new_word)
            # print(word)
            mapping[word] = new_word

        output_path = os.path.abspath(os.path.join(self.my_path, "../../..", "Dictionary of words Decomposed into biphones"))

        ordered_mapping = collections.OrderedDict(sorted(mapping.items()))
        my_excel_writer = ExcelGenerator.ExcelGenerator(os.path.join(output_path, "NEW Words Contain Syllables.xls"),
                                                        ordered_mapping, original_wordform_mapping,
                                                        syllable_key_mapping, biphone_mapping)
        my_csv_writer = CsvGenerator.CsvGenerator(os.path.join(output_path, "NEW Words Contain Syllables.csv"),
                                                  ordered_mapping, original_wordform_mapping, syllable_key_mapping,
                                                  biphone_mapping)
        print("Called Lazar Script")
