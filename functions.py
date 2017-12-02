'''
Created on 30 Mar 2017

@author: Bilisel
'''

import os

from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)
		
def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def easywrite(path,content,par = "w"):
    file = open(path,par)
    file.write(content) 
    file.close()

def delfiles(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

def delfile(file):
    if os.path.isfile(file):
        os.unlink(file)
