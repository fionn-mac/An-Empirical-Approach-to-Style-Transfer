from random import choices

with open('agatha-christie-sir-arthur-conan-doyle/Helper/agatha-christie-sir-arthur-conan-doyle-rep.txt') as f:
    lines = f.readlines()

all_scores = []

for line in lines:
    kaam = line.split(' ||| ')[1:]
    scores = [float(tup.split(' &&& ')[1].strip()) for tup in kaam]
    all_scores.append(sum(scores))

all_scores.sort()

counter = 0
for score in all_scores:
    if score < 0.95 and score > 0:
        counter += 1

print(counter, len(all_scores))
