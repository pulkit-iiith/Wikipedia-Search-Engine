import sys
import Stemmer
import re
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")
stemming = Stemmer.Stemmer('english')


def process(sentence,tag,word):
    full_data=sentence.split('#')
    flag=0

    for data in full_data:
        if tag is 'r':
            ans=re.findall(r'r[0-9]*',data,re.DOTALL)
            if len(ans)!=0:
                flag=1
        if tag is 't':
            ans=re.findall(r't[0-9]*',data,re.DOTALL)
            if len(ans)!=0:
                flag=1
        if tag is 'b':
            ans=re.findall(r'b[0-9]*',data,re.DOTALL)
            if len(ans)!=0:
                flag=1
        if tag is 'c':
            ans=re.findall(r'c[0-9]*',data,re.DOTALL)
            if len(ans)!=0:
                flag=1
        if tag is'e':
            ans=re.findall(r'e[0-9]*',data,re.DOTALL)
            if len(ans)!=0:
                flag=1 
        if tag is 'i':
            ans=re.findall(r'i[0-9]*',data,re.DOTALL)
            if len(ans)!=0:
                flag=1      

    if flag is 1:
        print(sentence)


def plain_query(inp,index_path):
    inp=inp.strip()
    lis=inp.split()
    tokens=[]
    for token in lis:
            wrd = stemmer.stem(token)
            tokens.append(wrd)
    file_pointer=open(index_path,'r')
    collect=file_pointer.readlines()
    for line in collect:
        pos=line.find('#')
        tempp=line[0:pos]
        tempp=tempp.strip()
        if tempp in tokens:
            print(line)


def field_query(inp,index_path):    
        field_dict={}
        temp='xyz' 
        collect=""
        for i in range(len(inp)):
            if inp[i]==':':
                if temp!='xyz':
                    field_dict[temp]=collect[0:len(collect)-1]
                    collect=""
                temp=inp[i-1]
                collect=""
            else:
                collect=collect+inp[i]
                
        if temp!='xyz':
            field_dict[temp]=collect
        final_dict={}
        for key,val in field_dict.items():
            val=val.strip()
            lis=val.split()
            tokens=[]
            for token in lis:
                wrd = stemmer.stem(token)
                tokens.append(wrd)
            for t in tokens:
                final_dict[t]=key
        fp=open(index_path,'r')
        lines=fp.readlines()
        for line in lines:
            idx=line.find('#')
            word=line[0:idx]
            word=word.strip()
            for key,val in final_dict.items():
                if key==word:
                    process(line,val,word)

        
def main():
    inp=sys.argv[2]
    index_path=sys.argv[1]+"/doc.txt"
    inp=inp.lower()
    filling=inp.find(":")
    if filling==-1:
      plain_query(inp,index_path)
    else:
      field_query(inp,index_path) 

if __name__=="__main__":
    main()

