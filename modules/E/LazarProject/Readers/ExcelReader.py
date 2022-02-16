from xlrd import open_workbook


class ExcelReader(object):
    def __init__(self, filename):
        self.work_book = open_workbook(filename)
        self.rows = self._get_rows()
        self.mapping = dict()
        self.reverse_mapping = dict()
        self.syllable_key_mapping = dict()
        self.biphone_mapping = dict()

        self.words = []
        for row in self.rows:
            # print("row0=", row[0])
            # print("row1= ", row[1])
            self.words.append(row[1].lower())
            self.mapping[row[0]] = row[1]
            self.reverse_mapping[row[1]] = row[0]
            self.syllable_key_mapping[row[1]] = row[0]
            self.biphone_mapping[row[1]] = row[2]



    def _get_rows(self):
        for s in self.work_book.sheets():
            values = []
            for row in range(2,s.nrows):
                # print(row)
                col_value = []
                for col in range(s.ncols):
                    value = (s.cell(row, col).value)
                    try:
                        value = str(int(value))

                    except:
                        pass
                    #print("value= ",value, "col_value= ",col_value)
                    col_value.append(value)
                values.append(col_value)
                # print(values)
            return values

    def get_mapping(self):
        #print(self.mapping)
        return self.mapping

    def get_reverse_mapping(self):
        return self.reverse_mapping

    def get_syllable_key_mapping(self):
        return self.syllable_key_mapping

    def get_biphone_mapping(self):
        return self.biphone_mapping

    def get_words_as_list(self):
        #print(self.words)
        return self.words
