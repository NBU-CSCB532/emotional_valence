import pandas as pd
from pandas import ExcelWriter, DataFrame
from pandas import ExcelFile
import excelWriter
from collections import defaultdict
from collections import namedtuple
import xlwt
style = xlwt.easyxf('pattern: pattern solid, fore_colour orange')

#my_excel_writer = excelWriter.ExcelGenerator("outputFinal.xls")
name="outputFinal.xls"
# read the excel files first
dataOUT = pd.read_excel(r'output.xls')
dfOUT: DataFrame = pd.DataFrame(dataOUT, columns=['Transcript PK', 'Syllable PK', 'Sequence PK'])
dOutput = defaultdict(list)
dDict = defaultdict(list)
dResult = defaultdict(list)

row=0
for index, line in dataOUT.iterrows():
    tOutput = namedtuple("output", ["Transcript", "Syllable", "Sequence"])
    #print("row= ", line["Transcript PK"], line["Syllable PK"], line['Sequence PK'])
    tuple_output = tOutput(Transcript=line["Transcript PK"] ,Syllable=line["Syllable PK"], Sequence=line['Sequence PK'])
    dOutput[index].append(tuple_output)
print(len(dOutput))

dataDict = pd.read_excel(r'dict.xlsx')
dfDict = pd.DataFrame(dataDict, columns=['WordForm', 'TranscriptAsFound', 'TranscriptToSyllableParer - without the ( )'])
for index, line in dfDict.iterrows():
    tdict = namedtuple("dict", ["WordForm", "TranscriptAsFound"])
    # print("row= ", line["Transcript PK"], line["Syllable PK"], line['Sequence PK'])
    tuple_dict = tdict(WordForm=line["WordForm"], TranscriptAsFound=line["TranscriptAsFound"])
    dDict[index].append(tuple_dict)
print(len(dDict))

# read the excel files first
dataSyllabe = pd.read_excel(r'Syllables2.xlsx')
dfSyllabe = pd.DataFrame(dataSyllabe, columns=['Syllable Key', 'Syllable', 'Souns Like'])

workbook = xlwt.Workbook()
sheet = workbook.add_sheet('Result')
row = 0
sheet.write(row, 0, "WordForm", style)
sheet.write(row, 1, "Transcript PK", style)
sheet.write(row, 2, "Syllable PK", style)
sheet.write(row, 3, "Sequence PK", style)
row += 1
for key, value in dDict.items():
    for item in value:
        for key1, value1 in dOutput.items():
            for item1 in value1:
                if item.TranscriptAsFound == item1.Transcript:
                    #print("word= ",item.WordForm, "Transcript= ", item1.Transcript, "Syllable = ", item1.Syllable, "Sequence= ", item1.Sequence)
                    tresult1 = namedtuple("result1", ["WordForm", "Transcript", "Syllable", "Sequence"])
                    # print("row= ", line["Transcript PK"], line["Syllable PK"], line['Sequence PK'])
                    tuple_result1 = tresult1(WordForm=item.WordForm,Transcript= item1.Transcript, Syllable=item1.Syllable, Sequence= item1.Sequence)
                    dResult[key1].append(tuple_result1)
                    sheet.write(row, 0, item.WordForm)
                    sheet.write(row, 1, item1.Transcript)
                    sheet.write(row, 2, item1.Syllable)
                    sheet.write(row, 3, item1.Sequence)
                    row += 1
workbook.save(name)

print(len(dResult))
