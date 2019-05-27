from sys import exit
from os import path

import argparse
import torch

from evaluation_loader import Evaluation_Loader
from train_network import Train_Network
from encoder_rnn import Encoder_RNN
from decoder_rnn import Decoder_RNN
from evaluate_model import Evaluate_Model

use_cuda = torch.cuda.is_available()

def load_weights(model, state_dict):
    own_state = model.state_dict()
    for name, param in state_dict.items():
        if name not in own_state or own_state[name].size() != param.size():
            print(name)
            continue

        # Backwards compatibility for serialized parameters.
        if isinstance(param, torch.nn.Parameter):
            param = param.data

        own_state[name].copy_(param)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-nl", "--num_layers", type=int, help="Number of layers in Encoder and Decoder", default=2)
    parser.add_argument("-z", "--hidden_size", type=int, help="GRU Hidden State Size", default=512)
    parser.add_argument("-dr", "--dropout", type=float, help="Dropout in decoder.", default=0.2)

    parser.add_argument("-d", "--dataset", type=str, help="Dataset directory.", default='../Datasets/OpenSubtitles/')

    parser.add_argument("-ep", "--encoder_parameters", type=str, help="Name of file containing encoder parameters.", default='encoder_tf_2.pt')
    parser.add_argument("-dp", "--decoder_parameters", type=str, help="Name of file containing decoder parameters.", default='decoder_tf_2.pt')

    args = parser.parse_args()

    print('Model Parameters:')
    print('Hidden Size                   :', args.hidden_size)
    print('Number of Layers              :', args.num_layers)
    print('--------------------------------------------\n')

    evaluation_loader = Evaluation_Loader(args.dataset)

    encoder = Encoder_RNN(args.hidden_size, (len(evaluation_loader.word2index), 300), batch_size=1,
                          num_layers=args.num_layers, use_embedding=False, train_embedding=False)
    decoder = Decoder_RNN(args.hidden_size, (len(evaluation_loader.word2index), 300), num_layers=args.num_layers,
                          use_embedding=False, train_embedding=False, dropout_p=args.dropout)

    if not args.encoder_parameters.endswith('.pt'): args.encoder_parameters += '.pt'
    if not args.decoder_parameters.endswith('.pt'): args.decoder_parameters += '.pt'

    args.encoder_parameters = path.join('../Pre_Train/', args.encoder_parameters)
    args.decoder_parameters = path.join('../Pre_Train/', args.decoder_parameters)

    if path.isfile(args.encoder_parameters) and path.isfile(args.decoder_parameters):
        load_weights(encoder, torch.load(args.encoder_parameters))
        load_weights(decoder, torch.load(args.decoder_parameters))

    else:
        print('One or more of the model parameter files are missing. Model cannot run in Evaluation mode.')
        exit(1)

    if use_cuda:
        encoder = encoder.cuda()
        decoder = decoder.cuda()

    train_network = Train_Network(encoder, decoder, evaluation_loader.index2word, num_layers=args.num_layers)

    evaluate_model = Evaluate_Model(train_network, evaluation_loader.word2index, evaluation_loader.index2word)

    print("Evaluating Network.")

    while(True):
        input_string = input("> ")
        evaluate_model.get_response(input_string.lower())
