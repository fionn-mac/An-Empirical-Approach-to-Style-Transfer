from os import system
from os import path
from os import listdir

from nltk.parse import CoreNLPParser
from nltk.tree import ParentedTree

def bfs(t, rules):
    try:
        current = t.label()

    except AttributeError:
        return

    else:
        production = ''
        for child in t:
            try:
                production += child.label() + ' '

            except AttributeError:
                pass

        production = production.strip()

        if len(production) > 0:
            if current not in rules:
                rules[current] = {}
                rules[current]['counter'] = 0

            if production not in rules[current]:
                rules[current][production] = 0

            rules[current][production] += 1
            rules[current]['counter'] += 1

        for child in t:
            bfs(child, rules)

if __name__ == "__main__":

    # Lexical parser.
    parser = CoreNLPParser(url='http://localhost:8080')

    authors = [file for file in listdir("../Authors-Dataset") if path.isfile(path.join("../Authors-Dataset", file)) and file.endswith('.txt')]

    for author in authors:
        file = path.join("../Authors-Dataset", author)
        lines = []
        rules = {}

        with open(file) as f:
            lines = f.readlines()

        for line in lines:
            if len(line) == 0:
                continue

            try:
                tokenized = parser.tokenize(line)
                parsed = parser.parse(tokenized)
                iterator = ParentedTree.convert(parsed)
                for tree in iterator:
                    bfs(tree, rules)

            except Exception as e:
                print(e)

        output_file = author[:-4] + '-analysis.txt'

        with open(output_file, 'w') as f:
            for i in rules:
                f.write(i + '\n')
                for j in rules[i]:
                    if j == 'counter':
                        continue

                    f.write('---> %s : %f\n' % (j, rules[i][j] / rules[i]['counter']))

                f.write('\n\n')
