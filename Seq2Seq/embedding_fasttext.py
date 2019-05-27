import torch
import numpy as np
from gensim.models import KeyedVectors

class Embedding_Fasttext(object):
    def __init__(self, word2index, file_path, out_of_vocab='out_of_vocab.txt'):
        self.file_path = file_path
        self.embedding_matrix = self.create_embed_matrix(word2index, out_of_vocab)

    def create_embed_matrix(self, word2index, out_of_vocab):
        word2vec = KeyedVectors.load_word2vec_format(self.file_path)
        # Fix embedding dimensions.
        embedding_matrix = np.zeros((len(word2index), 300))
        # embedding_matrix = np.random.rand(len(word2index), 300)

        with open(out_of_vocab, "w") as f:
            for word, i in word2index.items():
                if word not in word2vec.wv.vocab:
                    f.write(word + '\n')
                    continue

                embedding_matrix[i] = word2vec.word_vec(word)

        del word2vec
        embedding_matrix = torch.from_numpy(embedding_matrix).type(torch.FloatTensor)

        return embedding_matrix
