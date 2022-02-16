import re
from modules.E.LazarProject.config import SYLLABLE_REGEX_1, SYLLABLE_REGEX_2, SYLLABLE_REGEX_REVERSE

class SyllableFinder(object):
    mapping = dict()

    def __init__(self, word_list):
        for word in word_list:
            self.mapping[word] = []
            cleaned_word = re.sub(r'[\(\)ˈˌ]*', '', word, re.I | re.U | re.S | re.M)
            for pos in range(len(cleaned_word)):
                add_to_mapping = []
                try:
                    # print(word)
                    # print(cleaned_word)
                    add_to_mapping.append(cleaned_word[pos])
                    add_to_mapping.append(cleaned_word[pos] + cleaned_word[pos+1])
                    add_to_mapping.append(cleaned_word[pos] + cleaned_word[pos+1] + cleaned_word[pos+2])
                    add_to_mapping.append(cleaned_word[pos] + cleaned_word[pos+1] + cleaned_word[pos+2] + cleaned_word[pos+3])
                    # print(cleaned_word[pos]+' '+ cleaned_word[pos+1] +' '+ cleaned_word[pos+2] +' '+ cleaned_word[pos+3] +' '+  cleaned_word[pos+4])
                    add_to_mapping.append(cleaned_word[pos]+ cleaned_word[pos+1] + cleaned_word[pos+2] + cleaned_word[pos+3] + cleaned_word[pos+4])
                except IndexError:
                    pass
                self.mapping[word].append(add_to_mapping)



    def get_syllables_mapping(self):
        return self.mapping
