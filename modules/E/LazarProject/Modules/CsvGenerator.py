
class CsvGenerator(object):
    def __init__(self, name, mapping, original_wordform_mapping, syllable_key_mapping, biphone_mapping):
        f = open(name, 'w', newline='', encoding='UTF-8')
        f.write("{}, {}, {}, {}, {}, {}\n".format("WordFrom", "TranscriptSyl", "Syllable", "Sequence", "SyllableKey", "biphoneN"))
        for word, syllables in mapping.items():
            for i, s in enumerate(syllables):
                f.write("{}, {}, {}, {}, {}, {}\n".format(original_wordform_mapping[word], word, s, i+1, syllable_key_mapping[s], biphone_mapping[s]))
        f.close()