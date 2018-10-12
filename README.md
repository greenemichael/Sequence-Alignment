INPUT notes:
To run this program, the sequence files MUST be in the same folder as the program file 'HW2.py', files CANNOT be opened by passing their path to the program.

OUTPUT notes:
Program always outputs a text file 'out.txt' containing the new sequences (with gaps inserted) and their alignment score. If a match file is passed as well, the program runs anchored Needleman-Wunsch. The program will also ask the user before repeatedly permuting and realigning the sequences, ultimately creating a histogram of alignment scores. If executed, the output of this process is the file 'AlignmentScoreHistogram.pdf'.

***********************************************************************************
USAGE:
python HW2.py <name of reference FASTA file> <query FASTA file> [<match txt file>]
***********************************************************************************

Ex: python HW2.py Human_HOX.fa Fly_HOX.fa Match_HOX.txt
In this example the Human_HOX file becomes the reference sequence and Fly_HOX becomes the query. Match_HOX is used to run anchored needleman-wunsch for the two sequences.

Also acceptable: python HW2.py Human_HOX.fa Fly_HOX.fa
In this example, the non-anchored needleman-wunsch algorithm will be run for the two given files, with Human_HOX and Fly_HOX used as reference and query, respectively.