import xml.sax
import spacy
from nltk.stem import *
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import sys
import math
import copy
import Stemmer
import timeit

stemmer = SnowballStemmer("english")
stemming = Stemmer.Stemmer('english')
stop_words = set(stopwords.words('english'))


import re
r1 = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',re.DOTALL)
r2 = re.compile(r'{\|(.*?)\|}',re.DOTALL)
r3 = re.compile(r'{{v?cite(.*?)}}',re.DOTALL)
r4 = re.compile(r'[-.,:;_?()"/\']',re.DOTALL)
r5 = re.compile(r'\[\[file:(.*?)\]\]',re.DOTALL)
r6 = re.compile(r'[\'~` \n\"_!=@#$%-^*+{\[}\]\|\\<>/?]',re.DOTALL)
r7 = re.compile(r'{{infobox(.*?)}}',re.DOTALL)
r9 = re.compile(r'{{(.*?)}}',re.DOTALL)
r10 = re.compile(r'<(.*?)>',re.DOTALL)
r11=re.compile(r'\[\[(.*?)\]\]')



import xml.sax
import subprocess
import mwparserfromhell
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


inverted_index = {}

raw_text=0
clean_text=0

def clean(data):
    data = ' '.join(data)
    data = r4.sub(' ',data)
    data = r5.sub(' ',data)
    data = r6.sub(' ',data)
    data = data.split()
    return data

    
def add_in_inverted_index(dict_,tag,page_id):
    for i in dict_:
        if(i.isalnum()):
            if i not in inverted_index:
                inverted_index[i] = {}
            if page_id not in inverted_index[i]:
                inverted_index[i][page_id] = {}
            inverted_index[i][page_id][tag] = dict_[i]

class WikiXmlHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        xml.sax.handler.ContentHandler.__init__(self)
        self._buffer = None
        self._values = {}
        self._current_tag = None
        self._pages = []
        self.raw_index=0

    def characters(self, content):
        if self._current_tag:
            self._buffer.append(content)

    def startElement(self, name, attrs):
        if name in ('title', 'text'):
            self._current_tag = name
            self._buffer = []

    def endElement(self, name):
        if name == self._current_tag:
            self._values[name] = ' '.join(self._buffer)

        if name == 'page':
            self._pages.append((self._values['title'], self._values['text']))


def initial_preprocess(tex):
    tex = tex.lower()
    tex = r1.sub(' ', tex)
    tex = r2.sub(' ', tex)
    tex = r10.sub(' ', tex)
    tex.replace('\n', ' ')
    tex= tex.strip()
    return tex

def intermediate_preprocess(tex):
    tex = r3.sub(' ', tex)
    return tex


def fin_preprocess(tex):
    tex = r4.sub(' ', tex)
    tex = r5.sub(' ', tex)
    tex = r6.sub(' ', tex)
    tex = r7.sub(' ', tex)
    tex = tex.split()
    return tex



def create(pge,i):
    global raw_text,clean_text
    word_count=0
    Title_dict={}
    Body_Text_dict={}
    Infobox_dict={}
    Categories_dict={}
    External_Links_dict={}
    References_dict={}
    
    page_id=i
    title=pge[0]
    body=pge[1]
    title=title.lower()
    
    body=initial_preprocess(body)
    
    
    references=re.findall(r'{{v?cite(.*?)}}',body,re.DOTALL)


    for i in references:
        refer=re.findall(r'\| ?title ?=(.*?)\|',i,re.DOTALL) 
        str_refer=""
        str_refer=str_refer.join(refer)
        ref_tok=str_refer.split()
        raw_text+=len(ref_tok)
        ref_tok=clean(ref_tok)
        token_list=[]
        for w in ref_tok: 
            if w not in stop_words: 
                token_list.append(w)
        for token in token_list:
            word = stemmer.stem(token)
            if word.isalnum() and len(word)>1:
                if word not in References_dict:
                    References_dict[word]=1
                else:
                    References_dict[word]+=1
#     print(References_dict.keys())

        
    body=intermediate_preprocess(body)
    
    
    
    linkcontent=re.findall(r'== ?external links ?==.*',body,re.DOTALL)

    if len(linkcontent)!=0:
        linkcontent=r11.sub(' ',linkcontent[0])
        ll=re.findall(r'\[(.*?)\]', linkcontent, flags=re.MULTILINE)
        raw_text+=len(ll)
        ll=clean(ll)
        link=[]
        for w in ll: 
            if w not in stop_words: 
                link.append(w)
        for l in link:
            word=stemmer.stem(l)
            if word.isalnum() and len(word)>1:
                if l not in External_Links_dict:
                    External_Links_dict[l]=1
                else:
                    External_Links_dict[l]+=1
    
    
    categories = re.findall(r'\[\[category:(.*?)\]\]', body, flags=re.MULTILINE)
    
    for category in categories:
        tt = category.split()
        raw_text+=len(tt)
        tt = clean(tt)
        token_list=[]
        for w in tt: 
            if w not in stop_words: 
                token_list.append(w)
        for token in token_list:
            word = stemmer.stem(token)
            word.replace('\n', ' ')
            word= word.strip()
            if word.isalnum() and len(word)>1:
                if word not in Categories_dict:
                    Categories_dict[word] = 1
                else:
                    Categories_dict[word] += 1
    
    
    
    title = title.split()
    raw_text+=len(title)
    title=clean(title)
    for i in title:  
        word = stemmer.stem(i)  
        if word.isalnum() and len(word)>1:
            if word not in Title_dict:
                Title_dict[word] = 1
            else:
                Title_dict[word] += 1
    
    
    



    infobox = re.findall(r'{{infobox(.*?)}}', body, re.DOTALL)
    str_info=""
    str_info=str_info.join(infobox)
    
    pp=re.findall('^(.*?)\|',str_info)
    if(len(pp)>0):
        Infobox_dict[pp[0].strip()] = 1
    for infoList in infobox:
        tt = re.findall(r'=(.*?)\|',infoList,re.DOTALL)
        raw_text+=len(tt)
        tt = clean(tt)
        token_list=[]
        for w in tt: 
            if w not in stop_words: 
                token_list.append(w)
        for token in token_list:
                word = stemmer.stem(token)
                word.replace('\n', ' ')
                word= word.strip()
                if word.isalnum() and len(word)>1:
                        if word not in Infobox_dict:
                            Infobox_dict[word] = 1
                        else:
                            Infobox_dict[word] += 1
        
    
    body=fin_preprocess(body)
    raw_text+=len(body)
    fin_body=[]
    for w in body: 
        if w not in stop_words: 
            fin_body.append(w)

    for token in fin_body:
        word = stemmer.stem(token)
        word.replace('\n', ' ')
        word= word.strip()
        if word.isalnum() and len(word)>1:
            if word not in Body_Text_dict:
                Body_Text_dict[word] = 1
            else:
                Body_Text_dict[word] += 1
    
    
    add_in_inverted_index(Title_dict, "title", page_id)
    add_in_inverted_index(Body_Text_dict, "body", page_id)
    add_in_inverted_index(Infobox_dict, "infobox", page_id)
    add_in_inverted_index(Categories_dict, "category", page_id)
    add_in_inverted_index(External_Links_dict, "external_links", page_id)
    add_in_inverted_index(References_dict, "references", page_id)
    clean_text=len(inverted_index)


def store_index(path):  
    f=open(path+"/doc.txt",'w')
    indices=inverted_index.keys()
    indices=sorted(indices)

    for val in indices:
        sentence=" "
        sentence+=str(val)
        further_info=inverted_index[val]
        document_ids=further_info.keys()
        document_ids=sorted(document_ids)
        for each_id in document_ids:
            
            sentence+="#"+"D"+ str(each_id)
            inverted_index[val][each_id].keys()
            if(list(inverted_index[val][each_id].keys())[0])=="title":
                sentence+="t"+str(inverted_index[val][each_id]["title"])
            if(list(inverted_index[val][each_id].keys())[0])=="body":
                sentence+="b"+str(inverted_index[val][each_id]["body"])
            if(list(inverted_index[val][each_id].keys())[0])=="infobox":
                sentence+="i"+str(inverted_index[val][each_id]["infobox"])
            if(list(inverted_index[val][each_id].keys())[0])=="category":
                sentence+="c"+str(inverted_index[val][each_id]["category"])
            if(list(inverted_index[val][each_id].keys())[0])=="external_links":
                sentence+="e"+str(inverted_index[val][each_id]["external_links"])
            if(list(inverted_index[val][each_id].keys())[0])=="references":
                sentence+="r"+str(inverted_index[val][each_id]["references"])
        f.write(sentence + "\n")
    print("complete")
    f.close()
def wr(result):
    result_file=open(result,'w')
    result_file.write("raw_text :"+str(raw_text)+"words"+"\n")
    result_file.write("clean_text :"+str(clean_text)+"words"+"\n")
#     print(invertedIndex)
            
