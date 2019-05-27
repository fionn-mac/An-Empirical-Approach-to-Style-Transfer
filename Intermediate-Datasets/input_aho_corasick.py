from os import path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dataset", type=str, help="Path to Author data file.", default='../Authors-Dataset/Agatha-Christie.txt')
parser.add_argument("-r", "--replace_data", type=str, help="Path to paraphrase data file.", default='agatha-christie-sir-arthur-conan-doyle/Helper/agatha-christie-sir-arthur-conan-doyle-rep.txt')
parser.add_argument("-a", "--author", type=str, help="First author being considered.", default='agatha-christie')
args = parser.parse_args()

ppdb_data = set()
DATA_DIR = '/'.join(args.replace_data.split('/')[:-1])

with open(args.dataset) as f:
    author_lines = [' '.join(line.strip().split()) for line in f.readlines()]
    author_lines = ' | '.join(author_lines)

with open(args.replace_data) as f:
    lines = f.readlines()

    for line in lines:
        p1 = line.split(' ||| ')[0].strip()
        ppdb_data.add(' ' + ' '.join(p1.split()) + ' ')

with open(path.join(DATA_DIR, args.author + '-ac.txt'), 'w') as f:
    f.write(str(len(ppdb_data)) + '\n')

    for p in ppdb_data:
        f.write(p + '\n')

    f.write('1\n')
    f.write(author_lines + '\n')
