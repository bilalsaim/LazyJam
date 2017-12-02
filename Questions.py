'''
Created on 30 Mar 2017

@author: Bilisel
'''

class Questions:
    count = 0
    outfilestr = "Output.txt"
    infilestr = "Input-test.txt"
    copyfile = "Example.py"
    download = "tmp"
    operation = "Operation.txt"
    gpath = ""
    gname = ""
    
    
    def __init__(self,index,button):
        self.index = index
        self.letter = chr(65+index)
        self.path = Questions.gpath + "\\" + self.letter
        self.filename = Questions.gname + "-" + self.letter + ".py"
        self.file = self.path + "\\" + self.filename
        self.link = "https://code.google.com"+Questions.gbase+"/"+Questions.gid+"/dashboard#s=p"+str(index)
        self.button = button
        Questions.count = +1

    def opfile(self):
        return self.path + "\\" + Questions.operation
    
    def outfile(self):
        return self.path + "\\" + Questions.outfilestr

    def infile(self):
        return self.path + "\\" + Questions.infilestr

    def insmall(self):
        return self.letter + "-small-practice.in"

    def inlarge(self):
        return self.letter + "-large-practice.in"

    def outlarge(self):
        return self.path + "\\Output-large.txt"
        
    def outsmall(self):
        return self.path + "\\Output-small.txt"

    def copyexample(self):
        self.file 
    
    def __str__(self):
        return ""
