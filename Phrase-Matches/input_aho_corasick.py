import argparse
from nltk.corpus import stopwords

stop = set(stopwords.words('english'))

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dataset", type=str, help="Path to Author data file.", default='../Authors-Dataset/Agatha-Christie.txt')
parser.add_argument("-ppdb", "--paraphrase_data", type=str, help="Path to paraphrase data file.", default='../ppdb/m_dataset/m-keep.txt')
parser.add_argument("-a", "--author", type=str, help="First author being considered.", default='agatha-christie')
args = parser.parse_args()

ppdb_data = set()

with open(args.dataset) as f:
    author_lines = [' '.join(line.strip().split()) for line in f.readlines()]
    author_lines = ' | '.join(author_lines)

with open(args.paraphrase_data) as f:
    lines = f.readlines()

    for line in lines:
        [p1, p2] = line.split('|||')[1:3]

        p1 = p1.strip()
        p2 = p2.strip()

        if len(p1) <= 1 or len(p2) <= 1 or p1 in stop or p2 in stop:
            continue

        ppdb_data.add(' ' + ' '.join(p1.split()) + ' ')
        ppdb_data.add(' ' + ' '.join(p2.split()) + ' ')

with open('/home/vsareen/Code/Research/Last-Stand/Seq2Seq/Phrase-Matches/Intermediate/' + args.author + '-ac.txt', 'w') as f:
    f.write(str(len(ppdb_data)) + '\n')

    for p in ppdb_data:
        f.write(p + '\n')

    f.write('1\n')
    f.write(author_lines + '\n')
