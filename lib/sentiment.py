import re
import os

class sentiMeter():
    a = ""

    def __init__(self,a):
        self.a = a

    def countSentiStrength(self):
        a = self.a
        SentiPositive = 0
        SentiNegative = 0

        lokasi = os.path.dirname(os.path.abspath(__file__))
        f = open(lokasi + '/SentiStrength/SlangLookupTable.txt', encoding = "ISO-8859-1")
        for line in f:
            line = line.split('\t')
            if a.lower().find(line[0]) != -1:
                a = a.replace(line[0],line[1])

        f = open(lokasi + '/SentiStrength/EmotionLookupTable.txt', 'r')
        for line in f:
            line = line.split('\t')
            line[0] = line[0][:-1] if line[0].endswith("*") else line[0]
            if a.lower().find(line[0]) != -1:
                if int(line[1]) > 0:
                    SentiPositive = int(line[1]) if SentiPositive < int(line[1]) else SentiPositive
                else:
                    SentiNegative = int(line[1]) if SentiNegative > int(line[1]) else SentiNegative

        f = open(lokasi + '/SentiStrength/EmoticonLookupTable.txt', encoding = "ISO-8859-1")
        for line in f:
            line = line.split('\t')
            if a.lower().find(line[0]) != -1:
                if int(line[1]) > 0:
                    SentiPositive = int(line[1]) if SentiPositive < int(line[1]) else SentiPositive
                else:
                    SentiNegative = int(line[1]) if SentiNegative > int(line[1]) else SentiNegative
        #idiom
        f = open(lokasi + '/SentiStrength/IdiomLookupTable.txt', encoding = "ISO-8859-1")
        for line in f:
            line = line.split('\t')
            if a.lower().find(line[0]) != -1:
                if int(line[1]) > 0:
                    SentiPositive = int(line[1]) if SentiPositive < int(line[1]) else SentiPositive
                else:
                    SentiNegative = int(line[1]) if SentiNegative > int(line[1]) else SentiNegative

        f = open(lokasi + '/SentiStrength/QuestionWords.txt', encoding = "ISO-8859-1")
        for line in f:
            line = line.strip()
            if a.lower().find(line) != -1:
                SentiPositive = 1 if SentiPositive < 1 else SentiPositive
                SentiNegative = -1 if SentiNegative > -1 else SentiNegative

        f = open(lokasi + '/SentiStrength/BoosterWordList.txt', encoding = "ISO-8859-1")
        for line in f:
            line = line.split('\t')
            if a.lower().find(line[0]) != -1:
                if int(line[1]) > 0:
                    SentiPositive += int(line[1])
                else:
                    SentiNegative -= int(line[1])

        return [SentiPositive,SentiNegative]
