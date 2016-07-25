# -*- coding: utf-8 -*- 
import random
import pickle
import os
import sys

class Markov:
    def __init__(self, n=3):
        self.n = n
        self.data = {}

    def train(self, generator,):
        prev = ()
        try:
            while True:
                token = generator.next()
                for pprev in [prev[i:] for i in range(len(prev) + 1)]:
                    if not pprev in self.data:
                        self.data[pprev] = [0, {}]

                    if not token in self.data[pprev][1]:
                        self.data[pprev][1][token] = 0

                    self.data[pprev][1][token] += 1
                    self.data[pprev][0] += 1

                prev += (token,)
                if len(prev) > self.n:
                    prev = prev[1:]
        except:
            #generator has reached end
                return self.data 

    def generate(self, num_token=300, prev=None):
        res = []
        while len(res) < num_token:
            out = ""
            if prev is None:
                prev = ()
            try:
                out = self._selectToken(prev)
            except:
                #if prev composition is not in the data, shrink prev(until only one item)
                prev = prev[1:]
                out = self._selectToken(prev)
            prev += (out,)
            if out == "\n":
                prev = ()
            elif len(prev) > self.n:
                prev = prev[1:]
            res.append(out);
        return res

    def _selectToken(self, state):
        total, choices = self.data[state]
        idx = random.randrange(total)
        for token, freq in choices.items():
            if idx <= freq:
                return token
            idx -= freq

    def load(self, path):
        with open( path ) as f: 
            self.data = pickle.loads( f.read() )

    def save(self, path):
        with open( path, 'w' ) as f: 
            f.write( pickle.dumps( self.data ) )
