from os import path
from io import open
import unicodedata
import re

import torch

import numpy as np

class Evaluation_Loader(object):
    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.PAD_token = 0
        self.SOS_token = 1
        self.EOS_token = 2
        self.vocab = set(["<PAD>", "<SOS>", "<EOS>"])
        self.word2index = {"<PAD>" : 0, "<SOS>" : 1, "<EOS>" : 2}
        self.index2word = ["<PAD>", "<SOS>", "<EOS>"]
        self.vocab_size = 3
        self.load_vocabulary()

    def load_vocabulary(self):
        with open(path.join(self.dir_path, 'vocabulary.txt'), encoding='utf-8') as f:
            for word in f:
                word = word.strip('\n')
                self.vocab.add(word)
                self.index2word.append(word)
                self.word2index[word] = self.vocab_size
                self.vocab_size += 1
