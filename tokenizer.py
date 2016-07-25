# -*- coding: utf-8 -*- 
import markov
import pickle 
import jieba
import sys

#remove space and newline
def removeSpaceAndNewline(filename, newname):
    with open(filename) as fin:
        with open(newname,'w') as fout:
            for line in fin.readlines():
                line = line.strip()
                if line:
                    fout.write(line+'\n')
            fout.close()
        fin.close()

#wordMode = True : treat each word as a token
#wordMode = True : treat each character as a token
def tokenize(filename, wordMode=True):
    def charGen(content):
        for char in content:
            yield char

    with open(filename) as f:
        if wordMode:
            return jieba.cut(unicode(f.read(), "utf-8"))
        else:
            return charGen(unicode(f.read(), "utf-8"))

removeSpaceAndNewline('one.txt', 'neat-one.txt')
gen = tokenize('neat-one.txt', False)
mar = markov.Markov(3)
mar.train(gen)
res = mar.generate(1000)
print ''.join(res)