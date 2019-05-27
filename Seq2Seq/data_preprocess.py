from os import path
from io import open
import unicodedata
import re

import torch

import numpy as np
from nltk import word_tokenize

class Data_Preprocess(object):
    def __init__(self, src_text, dest_text, train_split=0.90):
        self.src_text = src_text
        self.dest_text = dest_text
        self.train_split = train_split
        self.PAD_token = 0
        self.SOS_token = 1
        self.EOS_token = 2
        self.vocab = set(["<PAD>", "<SOS>", "<EOS>"])
        self.word2index = {"<PAD>" : 0, "<SOS>" : 1, "<EOS>" : 2}
        self.index2word = ["<PAD>", "<SOS>", "<EOS>"]
        self.vocab_size = 3
        self.x_train = list()
        self.y_train = list()
        self.x_val = list()
        self.y_val = list()
        self.train_lengths = []
        self.val_lengths = []
        self.run()

    def convert_to_tensor(self, pairs):
        tensor_pairs = [[], []]
        lengths = []

        for i, tup in enumerate(pairs):
            tensor_pairs[0].append(torch.LongTensor(tup[0]))
            tensor_pairs[1].append(torch.LongTensor(tup[1]))
            lengths.append(len(tensor_pairs[0][-1]))

        return tensor_pairs[0], tensor_pairs[1], lengths

    def sort_and_tensor(self):
        xy_train = sorted(zip(self.x_train, self.y_train), key=lambda tup: len(tup[0]), reverse=True)
        xy_val = sorted(zip(self.x_val, self.y_val), key=lambda tup: len(tup[0]), reverse=True)

        self.x_train, self.y_train, self.train_lengths = self.convert_to_tensor(xy_train)
        self.x_val, self.y_val, self.val_lengths = self.convert_to_tensor(xy_val)

    def build_vocabulary(self, lines):
        for line in lines:
            for word in word_tokenize(line.lower()):
                word = word.strip()
                if word not in self.vocab:
                    self.vocab.add(word)
                    self.index2word.append(word)
                    self.word2index[word] = self.vocab_size
                    self.vocab_size += 1

    def convert_to_indices(self, lines):
        for i, line in enumerate(lines):
            indices = [self.word2index[word] for word in word_tokenize(line.lower())[:50]]
            lines[i] = indices

        return lines

    def load_data(self):
        with open(self.src_text) as f:
            actual_lines = f.readlines()

        with open(self.dest_text) as f:
            oriented_lines = f.readlines()

        assert len(actual_lines) == len(oriented_lines)

        self.build_vocabulary(actual_lines)
        self.build_vocabulary(oriented_lines)

        actual_lines = self.convert_to_indices(actual_lines)
        oriented_lines = self.convert_to_indices(oriented_lines)

        # If value < 1, taken as ratio of split. Otherwise taken as number of lines.
        if self.train_split < 1:
            self.train_split = int(self.train_split * len(actual_lines))

        return [actual_lines[:self.train_split], oriented_lines[:self.train_split]], \
               [actual_lines[self.train_split + 1:], oriented_lines[self.train_split + 1:]]

    def run(self):
        print('Loading data.')
        train_seq, val_seq = self.load_data()

        # Split to separate lists.
        self.x_train = train_seq[0]
        self.y_train = train_seq[1]
        self.x_val = val_seq[0]
        self.y_val = val_seq[1]

        self.sort_and_tensor()
