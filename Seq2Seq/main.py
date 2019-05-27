from os import path
import argparse

import torch

from data_preprocess import Data_Preprocess
from embedding_fasttext import Embedding_Fasttext
from encoder_rnn import Encoder_RNN
from decoder_rnn import Decoder_RNN
from train_network import Train_Network
from run_iterations import Run_Iterations

use_cuda = torch.cuda.is_available()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--num_iters", type=int, help="Number of iterations over the training set.", default=40)
    parser.add_argument("-nl", "--num_layers", type=int, help="Number of layers in Encoder and Decoder", default=2)
    parser.add_argument("-z", "--hidden_size", type=int, help="GRU Hidden State Size", default=512)
    parser.add_argument("-b", "--batch_size", type=int, help="Batch Size", default=32)
    parser.add_argument("-lr", "--learning_rate", type=float, help="Learning rate of optimiser.", default=1)
    parser.add_argument("-dr", "--dropout", type=float, help="Dropout in decoder.", default=0.2)

    parser.add_argument("-f", "--fold_size", type=int, help="Size of chunks into which training data must be broken.", default=500000)
    parser.add_argument("-tm", "--track_minor", type=bool, help="Track change in loss per cent of Epoch.", default=True)
    parser.add_argument("-tp", "--tracking_pair", type=bool, help="Track change in outputs over a randomly chosen sample.", default=True)
    parser.add_argument("-d", "--dataset", type=str, help="Dataset directory.", default='../Intermediate-Datasets/agatha-christie-sir-arthur-conan-doyle')
    parser.add_argument("-e", "--embedding_file", type=str, help="File containing word embeddings.", default='../Embeddings/Fasttext/crawl-300d-2M.vec')

    parser.add_argument("-a1", "--author_1", type=str, help="Name of author 1.", default='agatha-christie')
    parser.add_argument("-a2", "--author_2", type=str, help="Name of author 2.", default='sir-arthur-conan-doyle')
    parser.add_argument("-s", "--source", type=str, help="Source data (actual or oriented)", default='actual')

    args = parser.parse_args()

    print('Model Parameters:')
    print('Hidden Size                   :', args.hidden_size)
    print('Batch Size                    :', args.batch_size)
    print('Number of Layers              :', args.num_layers)
    print('Learning rate                 :', args.learning_rate)
    print('Number of Epochs              :', args.num_iters)
    print('--------------------------------------------\n')

    src_text = path.join(args.dataset, args.author_1 + '.txt')
    dest_text = path.join(args.dataset, args.author_2 + '-oriented-' + args.author_1 + '.txt')

    if args.source == 'oriented':
        src_text, dest_text = dest_text, src_text

    encoder_parameters = path.join(args.dataset, args.author_1 + '-' + args.author_2 + '-' + args.source + '-encoder.pt')
    decoder_parameters = path.join(args.dataset, args.author_1 + '-' + args.author_2 + '-' + args.source + '-decoder.pt')

    print('Reading input data.')
    data_p = Data_Preprocess(src_text, dest_text)

    print("Number of training Samples    :", len(data_p.x_train))
    print("Number of validation Samples  :", len(data_p.x_val))

    print('Creating Word Embedding.')

    ''' Use pre-trained word embeddings '''
    embedding = Embedding_Fasttext(data_p.word2index, args.embedding_file, out_of_vocab=args.author_1 + '-out-of-vocab.txt')

    encoder = Encoder_RNN(args.hidden_size, embedding.embedding_matrix, batch_size=args.batch_size,
                          num_layers=args.num_layers, use_embedding=True, train_embedding=False)
    decoder = Decoder_RNN(args.hidden_size, embedding.embedding_matrix, num_layers=args.num_layers,
                          use_embedding=True, train_embedding=False, dropout_p=args.dropout)

    # Delete embedding object post weight initialization in encoder and decoder
    del embedding

    if use_cuda:
        encoder = encoder.cuda()
        decoder = decoder.cuda()

    print("Training Network.")

    train_network = Train_Network(encoder, decoder, data_p.index2word, num_layers=args.num_layers)

    run_iterations = Run_Iterations(train_network, data_p.x_train, data_p.y_train, data_p.train_lengths,
                                    data_p.index2word, args.batch_size, args.num_iters, args.learning_rate,
                                    fold_size=args.fold_size, track_minor=args.track_minor, tracking_pair=args.tracking_pair,
                                    val_in_seq=data_p.x_val, val_out_seq=data_p.y_val, val_lengths=data_p.val_lengths)
    run_iterations.train_iters()
    run_iterations.evaluate_randomly()

    torch.save(encoder.state_dict(), encoder_parameters)
    torch.save(decoder.state_dict(), decoder_parameters)
