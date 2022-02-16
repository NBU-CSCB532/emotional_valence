import xlwt
style = xlwt.easyxf('pattern: pattern solid, fore_colour orange')

class ExcelGenerator(object):
    def __init__(self, name, mapping, original_wordform_mapping, syllable_key_mapping, biphone_mapping):
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('Result')
        row = 0
        sheet.write(row, 0, "WordForm", style)
        sheet.write(row, 1, "TranscriptSyl", style)
        sheet.write(row, 2, "Syllable", style)
        sheet.write(row, 3, "Sequence", style)
        sheet.write(row, 4, "SyllableKey", style)
        sheet.write(row, 5, "biphoneN", style)
        row += 1
        for word, syllables in mapping.items():
            for i, s in enumerate(syllables):
                if not s:
                    continue
                sheet.write(row, 0, original_wordform_mapping[word])
                sheet.write(row, 1, word)
                sheet.write(row, 2, s)
                sheet.write(row, 3, i+1)
                sheet.write(row, 4, syllable_key_mapping[s])
                sheet.write(row, 5, biphone_mapping[s])
                row += 1
        workbook.save(name)
