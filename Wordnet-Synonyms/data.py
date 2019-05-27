from os import path

import operator
import string

from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn

class Data(object):
    def __init__(self, file_path, vocab_file, vocab_size=None):
        self.file_path = file_path
        self.vocab_file = vocab_file
        self.pair2count = {}
        self.word2count = {}
        self.lines = []
        self.vocab = []
        self.vocab_size = vocab_size
        self.total_count = 0
        self.stop = stopwords.words('english') + list(string.punctuation)
        self.run()

    def get_wordnet_pos(self, treebank_tag):
        if treebank_tag.startswith('J'):
            return wn.ADJ
        elif treebank_tag.startswith('V'):
            return wn.VERB
        elif treebank_tag.startswith('N'):
            return wn.NOUN
        elif treebank_tag.startswith('R'):
            return wn.ADV
        else:
            return ''

    def create_vocabulary(self, line):
        # Lowercase, tokenize, and pos_tag input sentence.
        tagged = pos_tag(line.lower().split())

        for word, tag in tagged:
            if word in self.stop:
                continue

            wn_tag = self.get_wordnet_pos(tag)

            if (word, wn_tag) not in self.pair2count:
                self.pair2count[(word, wn_tag)] = 0
            self.pair2count[(word, wn_tag)] += 1

            if word not in self.word2count:
                self.word2count[word] = 0
            self.word2count[word] += 1

            self.total_count += 1

    def sort_trim_vocabulary(self):
        sorted_x = sorted(self.word2count.items(), key=operator.itemgetter(1), reverse=True)
        self.word2count.clear()

        # Set vocab_size to None to consider all words.
        for word, count in sorted_x[:self.vocab_size]:
            self.word2count[word] = count
            self.vocab.append(word)

        vocab_size = len(sorted_x)
        del sorted_x

        if not path.isfile(self.vocab_file):
            with open(self.vocab_file, "w") as v:
                v.write('Vocabulary size: %d\n\n' % vocab_size)

                for word in self.word2count:
                    v.write('%s : %d\n' % (word, self.word2count[word]))

    def run(self):
        with open(self.file_path) as f:
            self.lines = f.readlines()
            for line in self.lines:
                self.create_vocabulary(line)

        self.sort_trim_vocabulary()
