from nltk.corpus import wordnet as wn

class Synonyms(object):
    ''' author_n is an object of class Data '''
    def __init__(self, author_1, author_2, file_name):
        self.author_1 = author_1
        self.author_2 = author_2
        self.file_name = file_name
        self.word2ind = {}
        self.ind2word = []
        self.synonyms = []

    def create_synonym_sets(self):
        synonym_count = 0

        for word, wn_tag in self.author_1.pair2count.keys():
            # Search for synonyms only in case of words in vocabulary.
            if word not in self.author_1.word2count or len(word) < 2:
                continue

            if word not in self.word2ind:
                self.word2ind[word] = len(self.synonyms)
                self.ind2word.append(word)
                self.synonyms.append(dict())

            # The word itself must always be added in synonyms.
            if word in self.author_2.word2count:
                self.synonyms[self.word2ind[word]][word] = self.author_2.word2count[word] / self.author_2.total_count

            else:
                self.synonyms[self.word2ind[word]][word] = 0

            # No synset in case of invalid wordnet tag.
            if wn_tag == '':
                continue

            # List all synonyms, check if they are in second author's vocabulary, and add them if so.
            for syn in wn.synsets(word):
                for lemma in syn.lemmas():
                    synonym = lemma.name()

                    if len(synonym) < 2:
                        continue

                    if synonym in self.author_2.word2count:
                        self.synonyms[self.word2ind[word]][synonym] = self.author_2.word2count[synonym] / self.author_2.total_count
                        synonym_count += 1

        with open(self.file_name, 'a') as f:
            f.write('Average number of synonyms per word: %f\n\n' % (synonym_count / len(self.synonyms)))

    def get_synonym_info(self):
        with open(self.file_name, 'a') as f:
            for i, dictionary in enumerate(self.synonyms):
                f.write("%s" % self.ind2word[i])

                total_score = 0
                for synonym in dictionary.keys():
                    total_score += self.synonyms[i][synonym]

                for synonym in dictionary.keys():
                    score = self.synonyms[i][synonym]
                    if total_score != 0:
                        score = score / total_score

                    f.write(" ||| %s &&& %f" % (synonym, score))

                f.write('\n')
