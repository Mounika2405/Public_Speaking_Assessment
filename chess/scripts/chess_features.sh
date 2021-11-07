#!/bin/bash
#SBATCH --job-name=speech_model
#SBATCH -A research
#SBATCH --nodelist gnode07
#SBATCH -c 10
#SBATCH --gres gpu:1
#SBATCH --mem-per-cpu=2G
#SBATCH --time=48:00:00
#SBATCH --output=choutput.txt
#SBATCH --mail-user=mounikakankanti24@gmail.com    

echo "START"
echo "Loaded modules"
source env/bin/activate
module load python/3.7.4

echo "Started program execution"
python3 -W ignore chess/youtube_score/preprocess.py -dp /ssd_scratch/users/mounika.k/chess_audio/ -op chess_features_final.csv
echo "program executed"

