import pdftotext
import pandas as pd
import re
import os

class Extractword:
    
    def __init__(self):
        self.sheetEng = []
        self.sheetKor = []

        self.path = './test_papers'
        self.stop = ['Powered by TCPDF wwwtcpdforg']

    def extractword(self, content):
        '''시험지에서 영단어를 추출'''

        # Extract english words
        extEng = re.sub("[0-9]", "\n", content[1])
        extEng = re.sub("[^A-Za-z\n\ -]","", extEng)
        extEng = re.sub(" +", " ", extEng).split('\n')
        extEng = [word.rstrip(' ') for word in extEng if word != ' ' and word != '' and word not in self.stop]
        extEng = list(filter(None, extEng))[2:]

        extKor = re.sub("[0-9]", "==", content[0])
        extKor = re.sub("[^가-힣AB ,\;==]","", extKor)
        extKor = re.sub(" +", " ", extKor).split('==')
        extKor = list(filter(None, extKor))[4:]

        if len(extEng) > 20:
            self.sheetEng += [extEng[word] for word in range(0, len(extEng), 2)]
            self.sheetEng += [extEng[word] for word in range(1, len(extEng), 2)]

            self.sheetKor += [extKor[word] for word in range(0, len(extKor), 2)]
            self.sheetKor += [extKor[word] for word in range(1, len(extKor), 2)]
        else:
            self.sheetEng += extEng
            self.sheetKor += extKor

    def readPDF(self):
        '''test_papers 폴더에서 파일을 읽어 들임'''
        listdir = os.listdir(self.path)
        
        print("** File list **")
        for file in listdir:

            if file.split('.')[-1] == 'pdf':
                print(file)
                with open(os.path.join(self.path, file), 'rb') as pdf:
                    fileReader = pdftotext.PDF(pdf)
                self.extractword(fileReader)
        print("Length of sheet: ", len(self.sheetEng))
        self.save()       
    
    def save(self):
        if self.sheetEng or len(self.sheetEng) > 80:  # answersheet가 비어있지 않다면 / 그리고 
            df = pd.DataFrame(list(zip(self.sheetKor, self.sheetEng)))
            df.to_csv('answersheet.csv', index=False, header=False, encoding='utf-8-sig')
            
            print("To extract word is complete.")


if __name__ == '__main__':
    extword = Extractword()
    extword.readPDF()