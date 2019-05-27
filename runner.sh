
AUTHOR_1='agatha-christie'
AUTHOR_2='sir-arthur-conan-doyle'

source /home/vsareen/ProgramFiles/pytorch-pip/bin/activate

# Create -ac files which are input to aho_corasick
python ./Phrase-Matches/input_aho_corasick.py -d "./Authors-Dataset/$AUTHOR_1.txt" \
                                              -ppdb "./ppdb/m_dataset/m-keep.txt" \
                                              -a "$AUTHOR_1"
python ./Phrase-Matches/input_aho_corasick.py -d "./Authors-Dataset/$AUTHOR_2.txt" \
                                              -ppdb "./ppdb/m_dataset/m-keep.txt" \
                                              -a "$AUTHOR_2"

echo "Phrase Match inputs created."


# Run aho_corasick
./Phrase-Matches/a.out < "./Phrase-Matches/Intermediate/$AUTHOR_1-ac.txt" \
                       > "./Phrase-Matches/Intermediate/$AUTHOR_1-ac-out.txt"
./Phrase-Matches/a.out < "./Phrase-Matches/Intermediate/$AUTHOR_2-ac.txt" \
                       > "./Phrase-Matches/Intermediate/$AUTHOR_2-ac-out.txt"

echo "Aho Corasick run."

# Get phrase matches
python ./Phrase-Matches/phrase_match_count.py -d1 "./Phrase-Matches/Intermediate/$AUTHOR_1-ac.txt" \
                                              -c1 "./Phrase-Matches/Intermediate/$AUTHOR_1-ac-out.txt" \
                                              -d2 "./Phrase-Matches/Intermediate/$AUTHOR_2-ac.txt" \
                                              -c2 "./Phrase-Matches/Intermediate/$AUTHOR_2-ac-out.txt" \
                                              -ppdb "./ppdb/m_dataset/m-keep.txt" \
                                              -a1 $AUTHOR_1 \
                                              -a2 $AUTHOR_2

echo "ppdb phrase matches obtained."

# # Get wordnet synonym matches
# python ./Wordnet-Synonyms/main.py  -d1 "./Authors-Dataset/$AUTHOR_1.txt" \
#                                    -a1 "$AUTHOR_1" \
#                                    -d2 "./Authors-Dataset/$AUTHOR_2.txt" \
#                                    -a2 "$AUTHOR_2"
#
# echo "Wordnet Synonym sets obtained."

# Combine replacement data
python ./Intermediate-Datasets/combine_rep_data.py -a1 "$AUTHOR_1" -a2 "$AUTHOR_2"

echo "Replacement data combined."

# Create input files for modified aho_corasick
python ./Intermediate-Datasets/input_aho_corasick.py -d "./Authors-Dataset/$AUTHOR_1.txt" \
                                                     -r "./Intermediate-Datasets/$AUTHOR_1-$AUTHOR_2/Helper/$AUTHOR_1-$AUTHOR_2-rep.txt" \
                                                     -a "$AUTHOR_1"
python ./Intermediate-Datasets/input_aho_corasick.py -d "./Authors-Dataset/$AUTHOR_2.txt" \
                                                     -r "./Intermediate-Datasets/$AUTHOR_1-$AUTHOR_2/Helper/$AUTHOR_2-$AUTHOR_1-rep.txt" \
                                                     -a "$AUTHOR_2"

echo "Input files for modified aho corasick created."

# Get replacement indices using modified aho_corasick
./Intermediate-Datasets/a.out < "./Intermediate-Datasets/$AUTHOR_1-$AUTHOR_2/Helper/$AUTHOR_1-ac.txt" \
                              > "./Intermediate-Datasets/$AUTHOR_1-$AUTHOR_2/Helper/$AUTHOR_1-indices.txt"
./Intermediate-Datasets/a.out < "./Intermediate-Datasets/$AUTHOR_1-$AUTHOR_2/Helper/$AUTHOR_2-ac.txt" \
                              > "./Intermediate-Datasets/$AUTHOR_1-$AUTHOR_2/Helper/$AUTHOR_2-indices.txt"

echo "Phrase occurrence indices obtained."

# Get intermediate Texts (oriented data)
python ./Intermediate-Datasets/get_intermediate_data.py -d "./Intermediate-Datasets/$AUTHOR_1-$AUTHOR_2/Helper/$AUTHOR_1-ac.txt" \
                                                        -r "./Intermediate-Datasets/$AUTHOR_1-$AUTHOR_2/Helper/$AUTHOR_1-$AUTHOR_2-rep.txt" \
                                                        -i "./Intermediate-Datasets/$AUTHOR_1-$AUTHOR_2/Helper/$AUTHOR_1-indices.txt" \
                                                        -a1 "$AUTHOR_1" \
                                                        -a2  "$AUTHOR_2" \

echo "$AUTHOR_2 oriented $AUTHOR_1 data obtained."

python ./Intermediate-Datasets/get_intermediate_data.py -d "./Intermediate-Datasets/$AUTHOR_1-$AUTHOR_2/Helper/$AUTHOR_2-ac.txt" \
                                                        -r "./Intermediate-Datasets/$AUTHOR_1-$AUTHOR_2/Helper/$AUTHOR_2-$AUTHOR_1-rep.txt" \
                                                        -i "./Intermediate-Datasets/$AUTHOR_1-$AUTHOR_2/Helper/$AUTHOR_2-indices.txt" \
                                                        -a1 "$AUTHOR_2" \
                                                        -a2  "$AUTHOR_1" \

echo "$AUTHOR_1 oriented $AUTHOR_2 data obtained."
