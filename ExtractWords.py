import pdftotext
import pandas as pd
# import csv
import re
import os


class Extractword:
    

    def __init__(self):
        self.answersheet = []
        self.path = './test_papers'

    def extractword(self, content):
        ext = re.sub("[^a-z\n\ -]","", content[1])
        ext = re.sub(" +", " ", ext).split('\n')
        ext = [word for word in ext if word != ' ' and word != '']
        ext = list(filter(None, ext))[2:]
    
        if len(ext) > 20:
            self.answersheet += [ext[word] for word in range(0, len(ext), 2)]
            self.answersheet += [ext[word] for word in range(1, len(ext), 2)]

        else:
            self.answersheet += ext

    def readPDF(self):
        
        listdir = os.listdir(self.path)
        
        print("** File list **")
        for file in listdir:
            print(file)
            if file.split('.')[-1] == 'pdf':
                with open(os.path.join(self.path, file), 'rb') as pdf:
                    fileReader = pdftotext.PDF(pdf)
                self.extractword(fileReader)
        print("Length of sheet: ", len(self.answersheet))
        self.save()       

    
    def save(self):
        if self.answersheet or len(self.answersheet) > 80:  # answersheet가 비어있지 않다면 / 그리고 
            df = pd.DataFrame(self.answersheet)
            df.to_csv('answersheet.csv', index=False, header=False)
            
            print("To extract word is complete.")



if __name__ == '__main__':
    extword = Extractword()
    extword.readPDF()