from re import compile
from re import sub

from os import listdir
from os import path

from spacy.lang.en import English

ascii = compile(r"[^\x00-\x7F]+")
special = compile(r"[<>`\[\]\{\}\_\@\#\$\%\^\*\=\+\~]")

ascii = compile(r"[^\x00-\x7F]+")

spec_check = compile(r"[`\_\@\^\#\*\=\+\~\"]")
rem_paren = compile(r"[<\[\{].*[>\]\}]") # Remove anything contained within non-standard parenthesis. This is necessary as ppdb has some extra info in some lines.
# beginning_punc = compile(r"^\s*\W+")
# ending_punc = compile(r"\s*\W+$")
dollars = compile(r"\$(.*?)dollars")
dollar = compile(r"\$(.*?)dollar") # Remove any instances of dollar, make otherwise usable instances of a phrase useless.
useless_num = compile(r" [0-9]+\s*[\.,\?'\"\!](?![0-9a-zA-Z])")
single_alpha = compile(r"\s+[b-hj-zA-HJ-Z]\s+") # Must not remove a, i, and I

# Most of the dirtiness is due to messed up contractions, so we handle them all here.
ll = compile(r"(\w)\s+ll(\W)")
ll2 = compile(r"(\w)\s+'ll(\W)")
ve = compile(r"(\w)\s+ve(\W)")
ve2 = compile(r"(\w)\s+'ve(\W)")
re = compile(r"(\w)\s+re(\W)")
re2 = compile(r"(\w)\s+'re(\W)")
t = compile(r"(\w)\s+t(\W)")
t2 = compile(r"(\w)\s+'t(\W)")
d = compile(r"(\w)\s+d(\W)")
d2 = compile(r"(\w)\s+'d(\W)")
s = compile(r"(\w)\s+s(\W)")
s2 = compile(r"(\w)\s+'s(\W)")
m = compile(r"(\w)\s+m(\W)")
m2 = compile(r"(\w)\s+'m(\W)")
punct = compile(r"([^a-zA-Z0-9_\-\'])")

# Handle awkwardly space separated contractions.
arent = compile(r"(?:\s|^)([Aa])\s*r\s*e\s*n\s*'\s*t(?:\s|$)")
cant = compile(r"(?:\s|^)([Cc])\s*a\s*n\s*'\s*t(?:\s|$)")
didnt = compile(r"(?:\s|^)([Dd])\s*i\s*d\s*n\s*'\s*t(?:\s|$)")
dont = compile(r"(?:\s|^)([Dd])\s*o\s*n\s*'\s*t(?:\s|$)")
doesnt = compile(r"(?:\s|^)([Dd])\s*o\s*e\s*s\s*n\s*'\s*t(?:\s|$)")
hadnt = compile(r"(?:\s|^)([Hh])\s*a\s*d\s*n\s*'\s*t(?:\s|$)")
hasnt = compile(r"(?:\s|^)([Hh])\s*a\s*s\s*n\s*'\s*t(?:\s|$)")
havent = compile(r"(?:\s|^)([Hh])\s*a\s*v\s*e\s*n\s*'\s*t(?:\s|$)")
isnt = compile(r"(?:\s|^)([Ii])\s*s\s*n\s*'\s*t(?:\s|$)")
mustnt = compile(r"(?:\s|^)([Mm])\s*u\s*s\s*t\s*n\s*'\s*t(?:\s|$)")
neednt = compile(r"(?:\s|^)([Nn])\s*e\s*e\s*d\s*n\s*'\s*t(?:\s|$)")
shouldnt = compile(r"(?:\s|^)([Ss])\s*h\s*o\s*u\s*l\s*d\s*n\s*'\s*t(?:\s|$)")
wasnt = compile(r"(?:\s|^)([Ww])\s*a\s*s\s*n\s*'\s*t(?:\s|$)")
werent = compile(r"(?:\s|^)([Ww])\s*e\s*r\s*e\s*n\s*'\s*t(?:\s|$)")
wont = compile(r"(?:\s|^)([Ww])\s*o\s*n\s*'\s*t(?:\s|$)")
wouldnt = compile(r"(?:\s|^)([Ww])\s*o\s*u\s*l\s*d\s*n\s*'\s*t(?:\s|$)")
lets = compile(r"(?:\s|^)([Ll])\s*e\s*t\s*'\s*s(?:\s|$)")
im = compile(r"(?:\s|^)([Ii])\s*'\s*m(?:\s|$)")
id = compile(r"(?:\s|^)([Ii])\s*'\s*d(?:\s|$)")
ill = compile(r"(?:\s|^)([Ii])\s*'\s*l\s*l(?:\s|$)")
ive = compile(r"(?:\s|^)([Ii])\s*'\s*v\s*e(?:\s|$)")
hell = compile(r"(?:\s|^)([Hh])\s*e\s*'\s*l\s*l(?:\s|$)")
shell = compile(r"(?:\s|^)([Ss])\s*h\s*e\s*'\s*l\s*l(?:\s|$)")
hes = compile(r"(?:\s|^)([Hh])\s*e\s*'\s*s(?:\s|$)")
shes = compile(r"(?:\s|^)([Ss])\s*h\s*e\s*'\s*s(?:\s|$)")
hed = compile(r"(?:\s|^)([Hh])\s*e\s*'\s*d(?:\s|$)")
shed = compile(r"(?:\s|^)([Ss])\s*h\s*e\s*'\s*d(?:\s|$)")
youre = compile(r"(?:\s|^)([Yy])\s*o\s*u\s*'\s*r\s*e(?:\s|$)")
youll = compile(r"(?:\s|^)([Yy])\s*o\s*u\s*'\s*l\s*l(?:\s|$)")
youd = compile(r"(?:\s|^)([Yy])\s*o\s*u\s*'\s*d(?:\s|$)")
youve = compile(r"(?:\s|^)([Yy])\s*o\s*u\s*'\s*v\s*e(?:\s|$)")
were = compile(r"(?:\s|^)([Ww])\s*e\s*'\s*r\s*e(?:\s|$)")
well = compile(r"(?:\s|^)([Ww])\s*e\s*'\s*l\s*l(?:\s|$)")
wed = compile(r"(?:\s|^)([Ww])\s*e\s*'\s*d(?:\s|$)")
weve = compile(r"(?:\s|^)([Ww])\s*e\s*'\s*v\s*e(?:\s|$)")
theyll = compile(r"(?:\s|^)([Tt])\s*h\s*e\s*y\s*'\s*l\s*l(?:\s|$)")
theyre = compile(r"(?:\s|^)([Tt])\s*h\s*e\s*y\s*'\s*r\s*e(?:\s|$)")
theyd = compile(r"(?:\s|^)([Tt])\s*h\s*e\s*y\s*'\s*d(?:\s|$)")
theyve = compile(r"(?:\s|^)([Tt])\s*h\s*e\s*y\s*'\s*v\s*e(?:\s|$)")
its = compile(r"(?:\s|^)([Ii])\s*t\s*'\s*s(?:\s|$)")
itll = compile(r"(?:\s|^)([Ii])\s*t\s*'\s*l\s*l(?:\s|$)")
itd = compile(r"(?:\s|^)([Ii])\s*t\s*'\s*d(?:\s|$)")
therell = compile(r"(?:\s|^)([Tt])\s*h\s*e\s*r\s*e\s*'\s*l\s*l(?:\s|$)")
theres = compile(r"(?:\s|^)([Tt])\s*h\s*e\s*r\s*e\s*'\s*s(?:\s|$)")
thereve = compile(r"(?:\s|^)([Tt])\s*h\s*e\s*r\s*e\s*'\s*v\s*e(?:\s|$)")
thats = compile(r"(?:\s|^)([Tt])\s*h\s*a\s*t\s*'\s*s(?:\s|$)")
thatd = compile(r"(?:\s|^)([Tt])\s*h\s*a\s*t\s*'\s*d(?:\s|$)")
thatll = compile(r"(?:\s|^)([Tt])\s*h\s*a\s*t\s*'\s*l\s*l(?:\s|$)")

def replace_1(p):
    p = ascii.sub(" ", p)
    p = ' '.join(rem_paren.sub(r"", p).split())

    p = dollars.sub(r" \1 ", p)
    p = dollar.sub(r" \1 ", p)

    # p = beginning_punc.sub(r"", p)
    # p = ending_punc.sub(r"", p)

    p = p.replace('-lrb-', '').replace('-rrb-', '')

    return p

def contractions(p):
    p = ll.sub(r"\1'll\2", p)
    p = ve.sub(r"\1've\2", p)
    p = t.sub(r"\1't\2", p)
    p = re.sub(r"\1're\2", p)
    p = s.sub(r"\1's\2", p)
    p = d.sub(r"\1'd\2", p)
    p = m.sub(r"\1'm\2", p)
    p = ll2.sub(r"\1'll\2", p)
    p = ve2.sub(r"\1've\2", p)
    p = t2.sub(r"\1't\2", p)
    p = re2.sub(r"\1're\2", p)
    p = s2.sub(r"\1's\2", p)
    p = d2.sub(r"\1'd\2", p)
    p = m2.sub(r"\1'm\2", p)
    p = punct.sub(r" \1 ", p)

    p = arent.sub(r" \1ren't ", p)
    p = cant.sub(r" \1an't ", p)
    p = didnt.sub(r" \1idn't ", p)
    p = dont.sub(r" \1on't ", p)
    p = doesnt.sub(r" \1oesn't ", p)
    p = hadnt.sub(r" \1adn't ", p)
    p = hasnt.sub(r" \1asn't ", p)
    p = havent.sub(r" \1aven't ", p)
    p = isnt.sub(r" \1sn't ", p)
    p = mustnt.sub(r" \1ustn't ", p)
    p = neednt.sub(r" \1eedn't ", p)
    p = shouldnt.sub(r" \1houldn't ", p)
    p = wasnt.sub(r" \1asn't ", p)
    p = werent.sub(r" \1eren't ", p)
    p = wont.sub(r" \1on't ", p)
    p = wouldnt.sub(r" \1ouldn't ", p)
    p = lets.sub(r" \1et's ", p)
    p = im.sub(r" \1'm ", p)
    p = id.sub(r" \1'd ", p)
    p = ill.sub(r" \1'll ", p)
    p = ive.sub(r" \1've ", p)
    p = hell.sub(r" \1e'll ", p)
    p = shell.sub(r" \1he'll ", p)
    p = hes.sub(r" \1e's ", p)
    p = shes.sub(r" \1he's ", p)
    p = hed.sub(r" \1e'd ", p)
    p = shed.sub(r" \1he'd ", p)
    p = youre.sub(r" \1ou're ", p)
    p = youll.sub(r" \1ou'll ", p)
    p = youd.sub(r" \1ou'd ", p)
    p = youve.sub(r" \1ou've ", p)
    p = were.sub(r" \1e're ", p)
    p = well.sub(r" \1e'll ", p)
    p = wed.sub(r" \1e'd ", p)
    p = weve.sub(r" \1e've ", p)
    p = theyll.sub(r" \1hey'll ", p)
    p = theyre.sub(r" \1hey're ", p)
    p = theyd.sub(r" \1hey'd ", p)
    p = theyve.sub(r" \1hey've ", p)
    p = its.sub(r" \1t's ", p)
    p = itll.sub(r" \1t'll ", p)
    p = itd.sub(r" \1t'd ", p)
    p = therell.sub(r" \1here'll ", p)
    p = theres.sub(r" \1here's ", p)
    p = thereve.sub(r" \1here've ", p)
    p = thats.sub(r" \1hat's ", p)
    p = thatd.sub(r" \1hat'd ", p)
    p = thatll.sub(r" \1hat'll ", p)

    p = single_alpha.sub(r" ", p)

    return p

if __name__ == "__main__":

    MIN_SENT_LEN = 5
    # Initialize spacy sentence level tokenizer.
    tokenizer = English()
    tokenizer.add_pipe(tokenizer.create_pipe('sentencizer'))

    files = [file for file in listdir("../Authors-Dataset") if path.isfile(path.join("../Authors-Dataset", file)) and file.endswith('.txt')]

    for file in files:
        lines = []

        with open(file) as f:
            lines = f.readlines()

        with open(file, 'w') as f:
            for line in lines:
                sentences = []
                line = tokenizer(line)

                for sent in line.sents:
                    sent = replace_1(sent.string.strip())
                    sent = contractions(sent)

                    if len(sent.split()) > MIN_SENT_LEN: sentences.append(sent)

                for sentence in sentences:
                    f.write(sentence + '\n')

        print(file + " Done!")
