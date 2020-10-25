import create_index
import xml.sax
import timeit
import subprocess
import mwparserfromhell
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import Stemmer
import re
import sys
from pathlib import Path
import os



def main():
    data=sys.argv[1]
    index=sys.argv[2]
    result=sys.argv[3]
    #print(data)
    #print(index)
    #print(result)
    handler = create_index.WikiXmlHandler()
    parser = xml.sax.make_parser()
    parser.setContentHandler(handler)
    temp=os.listdir(data)
    dat=temp[0]
    i=0
    print("start_creation")
    for line in subprocess.Popen(['bzcat'], 
                              stdin = open(data+"/"+dat), 
                              stdout = subprocess.PIPE).stdout:
        parser.feed(line)
        if len(handler._pages)>i:
                create_index.create(handler._pages[i],i)
                i+=1
                print(i)
                #if(i>10):
                  #break
    print("store_creation")
    create_index.store_index(index)
    result_file=open(result,'w')
    print("write")
    create_index.wr(result)

    
if __name__ == "__main__": 
	main() 
