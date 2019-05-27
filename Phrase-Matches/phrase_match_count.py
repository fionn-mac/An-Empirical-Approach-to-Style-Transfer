from os import path
import argparse
from nltk.corpus import stopwords

stop = set(stopwords.words('english'))

def insert(dct, p1, p2, score):
    if p1 not in dct:
        dct[p1] = dict()

    if p2 not in dct:
        dct[p2] = dict()

    if p1 not in dct[p2]:
        dct[p2][p1] = score

    dct[p1][p2] = score

def get_ppdb_data(file_path):
    ppdb_data = {}

    with open(file_path) as f:
        lines = f.readlines()
        for line in lines:
            [p1, p2, score] = line.split('|||')[1:]
            p1 = p1.strip()
            p2 = p2.strip()

            if len(p1) <= 1 or len(p2) <= 1 or p1 in stop or p2 in stop:
                continue

            p1 = ' ' + ' '.join(p1.split()) + ' '
            p2 = ' ' + ' '.join(p2.split()) + ' '

            insert(ppdb_data, p1, p2, float(score))

    return ppdb_data

def add_phrases(data_file, count_file):
    phrase2count = {}
    total_count = 0

    with open(data_file) as f:
        lines = [line.strip('\n') for line in f.readlines()]
        count = int(lines[0])

        phrases = lines[1:count + 1]
        del lines

    with open(count_file) as f:
        counts = [int(num.strip()) for num in f.readlines()[1:]]

    assert len(phrases) == len(counts)

    for p, c in zip(phrases, counts):
        phrase2count[p] = c
        total_count += c

    return phrase2count, total_count

def get_match_scores(file_name, ppdb_data, a1_phrase2count, a2_phrase2count):
    phrase_matches = []
    phrase2ind = {}
    ind2phrase = []

    phrase_match_count = 0
    counter = 0

    for p1 in a1_phrase2count.keys():
        if a1_phrase2count[p1] == 0:
            continue

        phrase2ind[p1] = counter
        ind2phrase.append(p1)
        phrase_matches.append(dict())
        counter += 1

        # The phrase itself must always be added in phrase_matches.
        phrase_matches[phrase2ind[p1]][p1] = a2_phrase2count[p1] * 100 / a2_p_count

        for p2 in ppdb_data[p1]:
            if a2_phrase2count[p2] > 0:
                phrase_matches[phrase2ind[p1]][p2] = a2_phrase2count[p2] * ppdb_data[p1][p2] * 100 / a2_p_count
                phrase_match_count += 1

    with open(file_name, 'w') as f:
        f.write('Average number of matches per phrase: %f\n\n' % (phrase_match_count / len(phrase_matches)))

    with open(file_name, 'a') as f:
        for i, dictionary in enumerate(phrase_matches):
            f.write("%s" % ind2phrase[i])

            total_score = 0
            for phrase in dictionary.keys():
                total_score += phrase_matches[i][phrase]

            for phrase in dictionary.keys():
                score = phrase_matches[i][phrase]
                if total_score != 0:
                    score = score / total_score

                f.write(" ||| %s &&& %f" % (phrase, score))

            f.write('\n')

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-d1", "--dataset_1", type=str, help="Path to first data file.", default='Intermediate/agatha-christie-ac.txt')
    parser.add_argument("-c1", "--count_1", type=str, help="Path to first count file.", default='Intermediate/agatha-christie-ac-out.txt')
    parser.add_argument("-c2", "--count_2", type=str, help="Path to second count file.", default='Intermediate/sir-arthur-conan-doyle-ac-out.txt')
    parser.add_argument("-d2", "--dataset_2", type=str, help="Path to second data file.", default='Intermediate/sir-arthur-conan-doyle-ac.txt')
    parser.add_argument("-ppdb", "--paraphrase_data", type=str, help="Path to paraphrase data file.", default='../ppdb/m_dataset/m-keep.txt')
    parser.add_argument("-a1", "--author_1", type=str, help="First author being considered.", default='agatha-christie')
    parser.add_argument("-a2", "--author_2", type=str, help="Second author being considered.", default='sir-arthur-conan-doyle')
    args = parser.parse_args()

    a1_phrase2count, a1_p_count = add_phrases(args.dataset_1, args.count_1)
    a2_phrase2count, a2_p_count = add_phrases(args.dataset_2, args.count_2)

    ppdb_data = get_ppdb_data(args.paraphrase_data)

    get_match_scores(path.join('/home/vsareen/Code/Research/Last-Stand/Seq2Seq/Intermediate-Datasets/' + args.author_1 + '-' + args.author_2 + '/Helper' , args.author_1 + '-' + args.author_2 + '-phrases.txt'), ppdb_data, a1_phrase2count, a2_phrase2count)
    get_match_scores(path.join('/home/vsareen/Code/Research/Last-Stand/Seq2Seq/Intermediate-Datasets/' + args.author_1 + '-' + args.author_2 + '/Helper' , args.author_2 + '-' + args.author_1 + '-phrases.txt'), ppdb_data, a2_phrase2count, a1_phrase2count)
