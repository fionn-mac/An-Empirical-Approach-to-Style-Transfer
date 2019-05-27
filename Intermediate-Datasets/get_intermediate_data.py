from os import path
import random

import argparse

def read_replacement_data(data_file):
    data = {}

    with open(data_file) as f:
        lines = f.readlines()

    for line in lines:
        if line.startswith('Average number of'):
            continue

        line = line.split(' ||| ')
        phrase = ' ' + line[0].strip() + ' '

        if len(phrase) == 0:
            continue

        rep_info = []
        for rep in line[1:]:
            rep = rep.split(' &&& ')
            rep_info.append((' ' + rep[0].strip() + ' ', float(rep[1].strip())))

        data[phrase] = tuple(rep_info)

    return data

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dataset", type=str, help="Path to Author data file.", default='agatha-christie-sir-arthur-conan-doyle/Helper/agatha-christie-ac.txt')
parser.add_argument("-r", "--replace_data", type=str, help="Path to paraphrase data file.", default='agatha-christie-sir-arthur-conan-doyle/Helper/agatha-christie-sir-arthur-conan-doyle-rep.txt')
parser.add_argument("-i", "--index_file", type=str, help="Path to index file.", default='agatha-christie-sir-arthur-conan-doyle/Helper/agatha-christie-indices.txt')
parser.add_argument("-a1", "--author_1", type=str, help="First author being considered.", default='agatha-christie')
parser.add_argument("-a2", "--author_2", type=str, help="Second author being considered.", default='sir-arthur-conan-doyle')
args = parser.parse_args()

DATA_DIR = '/'.join(args.dataset.split('/')[:-2])
phrases = []

with open(args.dataset) as f:
    lines = f.readlines()
    author_data = lines[-1].strip()
    phrases = [phrase.strip('\n') for phrase in lines[1:-2]]

    del lines

rep_data = read_replacement_data(args.replace_data)

with open(args.index_file) as f:
    indices = [int(ind.strip()) for ind in f.readlines()[0].split()]

base = 0
final_author_data = []
comparison_author_data = []
total = len(indices)

for i, ind in enumerate(indices):
    if ind == -1:
        continue

    phrase = phrases[ind]
    range = len(phrase)

    replacements = [tup[0] for tup in rep_data[phrase]]
    weights = [tup[1] for tup in rep_data[phrase]]

    if sum(weights) < 0.0001:
        rep = random.choice(replacements)

    else:
        rep = random.choices(population=replacements, weights=weights)[0]

    # Must update index value according to change in length.
    final_author_data.append(author_data[base:i - range + 1] + rep)
    # print(phrase, ' | ', rep, ' | ', author_data[base : i + 1], ' | ', final_author_data[-1])
    # print(author_data[base : i + 1])
    # print(final_author_data[-1])
    base = i + 1

if base < i + 1:
    final_author_data.append(author_data[base:i + 1])

final_author_data = ''.join(final_author_data)

output_file = args.author_2 + '-oriented-' + args.author_1 + '.txt'
output_file = path.join(DATA_DIR, output_file)

with open(output_file, 'w') as f:
    for line in final_author_data.split(' | '):
        f.write(line + '\n')
