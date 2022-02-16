VOWELS = 'ɑaeuyioɒæɪʊɔəɜʌy'
NON_VOWELS = 'ʒ|tʃ|dʒ'
NON_VOWELS_FULL = NON_VOWELS + 'bcdfghjklmnnpqrstvxz'
SYLLABLE_REGEX_1 = r'(?:[{vowels}]{{1,2}}\ː?(?:(?:{nonvowels})|[^{vowels}:]))'.format(vowels=VOWELS, nonvowels=NON_VOWELS)
SYLLABLE_REGEX_2 = r'(?:[{vowels}][{nonvowels}])'.format(vowels=VOWELS, nonvowels=NON_VOWELS_FULL)
SYLLABLE_REGEX_REVERSE = r'(?:[{nonvowels}][{vowels}])'.format(vowels=VOWELS, nonvowels=NON_VOWELS_FULL)