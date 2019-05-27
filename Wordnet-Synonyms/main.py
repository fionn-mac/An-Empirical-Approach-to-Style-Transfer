from os import path
import argparse

import torch

from data import Data
from synonyms import Synonyms

use_cuda = torch.cuda.is_available()

def analyse_vocabularies(data_1, data_2, file_name):
    with open(file_name, 'w') as f:
        f.write('Data Statistics:\n')

        f.write('Most frequent word in Dataset 1: ' + data_1.vocab[0] + ' with count: ' + str(data_1.word2count[data_1.vocab[0]]) + '\n')
        f.write('Most frequent word in Dataset 2: ' + data_2.vocab[0] + ' with count: ' + str(data_2.word2count[data_2.vocab[0]]) + '\n')

        f.write('Least frequent word in Dataset 1: ' + data_1.vocab[-1] + ' with count: ' + str(data_1.word2count[data_1.vocab[-1]]) + '\n')
        f.write('Least frequent word in Dataset 2: ' + data_2.vocab[-1] + ' with count: ' + str(data_2.word2count[data_2.vocab[-1]]) + '\n')

        count = 0
        for word in data_1.vocab:
            if word in data_2.word2count:
                count += 1

        f.write("\nTotal number of words in common: %d\n\n" % count)

        f.write('Common words:\n')
        for word in data_1.vocab:
            if word in data_2.word2count:
                f.write("Word: %s Count in Dataset 1: %d Count in Dataset 2: %d\n" % (word, data_1.word2count[word], data_2.word2count[word]))
        f.write('\n')

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-d1", "--dataset_one", type=str, help="Path to first data file.", default='../Authors-Dataset/Agatha-Christie.txt')
    parser.add_argument("-d2", "--dataset_two", type=str, help="Path to second data file.", default='../Authors-Dataset/Sir-Arthur-Conan-Doyle.txt')
    parser.add_argument("-a1", "--author_one", type=str, help="First author being considered.", default='agatha-christie')
    parser.add_argument("-a2", "--author_two", type=str, help="Second author being considered.", default='sir-arthur-conan-doyle')
    args = parser.parse_args()

    print('Reading input data.')
    file_name = path.join('/home/vsareen/Code/Research/Last-Stand/Seq2Seq/Intermediate-Datasets/' + args.author_one + '-' + args.author_two + '/Helper/', args.author_one + '-vocab.txt')
    data_1 = Data(args.dataset_one, file_name)
    file_name = path.join('/home/vsareen/Code/Research/Last-Stand/Seq2Seq/Intermediate-Datasets/' + args.author_one + '-' + args.author_two + '/Helper/', args.author_two + '-vocab.txt')
    data_2 = Data(args.dataset_two, file_name)

    file_name = path.join('/home/vsareen/Code/Research/Last-Stand/Seq2Seq/Intermediate-Datasets/' + args.author_one + '-' + args.author_two + '/Helper/', args.author_one + '-' + args.author_two + '-analysis.txt')
    analyse_vocabularies(data_1, data_2, file_name)

    file_name = path.join('/home/vsareen/Code/Research/Last-Stand/Seq2Seq/Intermediate-Datasets/' + args.author_one + '-' + args.author_two + '/Helper/', args.author_one + '-' + args.author_two + '-synonyms.txt')
    synonyms = Synonyms(data_1, data_2, file_name)
    synonyms.create_synonym_sets()
    synonyms.get_synonym_info()

    file_name = path.join('/home/vsareen/Code/Research/Last-Stand/Seq2Seq/Intermediate-Datasets/' + args.author_one + '-' + args.author_two + '/Helper/', args.author_two + '-' + args.author_one + '-synonyms.txt')
    synonyms = Synonyms(data_2, data_1, file_name)
    synonyms.create_synonym_sets()
    synonyms.get_synonym_info()
