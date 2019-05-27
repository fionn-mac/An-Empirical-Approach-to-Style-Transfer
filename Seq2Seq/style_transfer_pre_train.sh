#!/bin/bash
#SBATCH -A Research
#SBATCH -n 8
#SBATCH --gres=gpu:1
#SBATCH --mem-per-cpu=3072
#SBATCH -t 4-00:00:00

AUTHOR_1='agatha-christie'
AUTHOR_2='sir-arthur-conan-doyle'
SOURCE='actual'

# AUTHOR_1='sir-arthur-conan-doyle'
# AUTHOR_2='agatha-christie'
# SOURCE='oriented'

OUTPUT_FILE="$AUTHOR_1-$AUTHOR_2.txt"

module add cuda/9.0
module add cudnn/7-cuda-9.0
source /home/aditya.bharti/pytorch-pip/bin/activate
python -u main.py -a1 "$AUTHOR_1" -a2 "$AUTHOR_2" -s "$SOURCE" > "$OUTPUT_FILE"
