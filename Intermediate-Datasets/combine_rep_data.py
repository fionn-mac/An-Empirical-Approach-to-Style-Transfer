from os import path
import argparse

def read_replacement_data(data_file):
    data = {}

    with open(data_file) as f:
        lines = f.readlines()

    for line in lines:
        if line.startswith('Average number of'):
            continue

        line = line.split(' ||| ')
        phrase = line[0].strip()

        if len(phrase) == 0:
            continue

        rep_info = []
        for rep in line[1:]:
            rep = rep.split(' &&& ')
            rep_info.append((rep[0].strip(), float(rep[1].strip())))

        data[phrase] = tuple(rep_info)

    return data

def combine_phrase_syn_dicts(phrase_dict, syn_dict):
    final_dict = {}
    keys = list(phrase_dict.keys())

    for item in keys:
        if item in syn_dict:
            temp1 = phrase_dict.pop(item)
            temp2 = syn_dict.pop(item)

            total = sum([tup[1] for tup in temp1]) + sum([tup[1] for tup in temp2])
            total = max(total, 1.0)

            intersect_dict = {}

            for tup in (*temp1, *temp2):
                if tup[0] not in intersect_dict:
                    intersect_dict[tup[0]] = 0
                intersect_dict[tup[0]] += tup[1] / total

            tup = []
            for key in intersect_dict:
                tup.append((key, intersect_dict[key]))

            final_dict[item] = tuple(tup)
            del intersect_dict

    return {**final_dict, **phrase_dict, **syn_dict}

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-a1", "--author_1", type=str, help="First author being considered.", default='agatha-christie')
    parser.add_argument("-a2", "--author_2", type=str, help="Second author being considered.", default='sir-arthur-conan-doyle')
    args = parser.parse_args()

    DATA_DIR = '/home/vsareen/Code/Research/Last-Stand/Seq2Seq/Intermediate-Datasets/' + args.author_1 + '-' + args.author_2
    HELPER_DIR = '/home/vsareen/Code/Research/Last-Stand/Seq2Seq/Intermediate-Datasets/' + args.author_1 + '-' + args.author_2 + '/Helper'

    phrase12 = path.join(HELPER_DIR, args.author_1 + '-' + args.author_2 + '-phrases.txt')
    phrase21 = path.join(HELPER_DIR, args.author_2 + '-' + args.author_1 + '-phrases.txt')

    syn12 = path.join(HELPER_DIR, args.author_1 + '-' + args.author_2 + '-synonyms.txt')
    syn21 = path.join(HELPER_DIR, args.author_2 + '-' + args.author_1 + '-synonyms.txt')

    print('Combining replacement data from author 2 wrt author 1.')
    phrase_data = read_replacement_data(phrase12)
    syn_data = read_replacement_data(syn12)

    rep_data = combine_phrase_syn_dicts(phrase_data, syn_data)
    del phrase_data, syn_data

    rep_file = path.join(HELPER_DIR, args.author_1 + '-' + args.author_2 + '-rep.txt')

    with open(rep_file, 'w') as f:
        for key in rep_data.keys():
            f.write("%s" % key)

            for tup in rep_data[key]:
                f.write(" ||| %s &&& %f" % (tup[0], tup[1]))

            f.write('\n')

    del rep_data

    print('Combining replacement data from author 1 wrt author 2.')
    phrase_data = read_replacement_data(phrase21)
    syn_data = read_replacement_data(syn21)

    rep_data = combine_phrase_syn_dicts(phrase_data, syn_data)
    del phrase_data, syn_data

    rep_file = path.join(HELPER_DIR, args.author_2 + '-' + args.author_1 + '-rep.txt')

    with open(rep_file, 'w') as f:
        for key in rep_data.keys():
            f.write("%s" % key)

            for tup in rep_data[key]:
                f.write(" ||| %s &&& %f" % (tup[0], tup[1]))

            f.write('\n')
