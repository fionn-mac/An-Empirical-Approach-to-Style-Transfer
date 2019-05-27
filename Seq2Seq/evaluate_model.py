import time
import random

import torch
import torch.nn as nn
from torch import optim
import numpy as np

from nltk import bleu_score
from nltk import word_tokenize

from helper import Helper

class Evaluate_Model(object):
    def __init__(self, model, word2index, index2word,):
        self.use_cuda = torch.cuda.is_available()
        self.model = model
        self.word2index = word2index
        self.index2word = index2word
        self.help_fn = Helper()

    def convert_to_tensor(self, sequence):
        indices = []
        for word in word_tokenize(sequence):
            if word in self.word2index:
                indices.append(self.word2index[word])
            else:
                indices.append(self.word2index["UNK"])

        sequence = torch.LongTensor(indices)
        if self.use_cuda:
            sequence = sequence.cuda()
        return sequence

    def evaluate(self, in_seq):
        return self.model.get_response(in_seq)

    def get_response(self, in_seq):
        self.model.encoder.eval()
        self.model.decoder.eval()

        in_seq = self.convert_to_tensor(in_seq)
        output_words = self.evaluate([in_seq])
        try:
            target_index = output_words[0].index('<EOS>') + 1
        except ValueError:
            target_index = len(output_words[0])

        # TODO: Remove this false target_index
        target_index = len(output_words[0])

        output_words = output_words[0][:target_index]

        output_sentence = ' '.join(output_words)
        print('< ', output_sentence)
