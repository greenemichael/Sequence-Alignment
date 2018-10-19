# Project contents:
- Python source code
- Sample input .txt files (sequence and match file samples) to show required format
- Sample output .txt and .pdf files (produced from running the program on the sample files)
- FASTA files for human and mouse TITIN protein sequences (TITIN is the largest known protein, ~30,000 amino acids in length)
- Match file for the TITIN sequences
- Output for aligning human and mouse TITIN sequences
- This...

# GLOBAL SEQUENCE ALIGNMENT notes:
The task this accomplishes can be described as inserting gaps into either of two sequences of DNA/RNA or amino acids such that the resulting strings have an optimal similarity score. Imagine aligning two sequences of genes, **ACGAD** and **ACAD**: to perform further meaningful biological analyses, they need to be aligned as **ACGAD** and **AC_AD** because it minimizes mismatches.

This task is important in genomics because the alignment and similarity score of two genes can indicate homologous pairs, suggesting an evolutionary relationship between the organisms each sequence came from. These scores can be further used to contruct phylogenetic trees for entire ecosystems.

To accomplish this task, the Needleman-Wunsch algorithm is implemented, as well as an anchored version. Anchored Needleman-Wunsch assumes some regions ('anchors') are known to match in both sequences, and the algorithm takes as input the start and end positions of each anchor as well as the two sequences to be aligned. The task of sequence alignment then becomes aligning the regions between anchors and building up the final alignment, saving time.

If desired, this program will also permute both sequences, perform alignment & scoring, and repeat 10,000 times. The resulting 10,000 scores are then made into a histogram and saved to a PDF file. This is simply to show that the algorithm is producing an alignment that scores significantly higher than if the alignment was random.

## INPUT notes:
To run this program, the sequence files MUST be in the same folder as the program file 'SequenceAlignment.py', files CANNOT be opened by passing their path to the program. Input files must have the same format as the sample files. While the included TITIN files will work with this program, **_it is recommended to use the sample format instead of that in the TITIN files._**

## OUTPUT notes:
Program always outputs a text file 'out.txt' containing the new sequences (with gaps inserted) and their alignment score. If a match file is passed as well, the program runs anchored Needleman-Wunsch. The program will also ask the user before repeatedly permuting and realigning the sequences, ultimately creating a histogram of alignment scores. If this last step is executed, the output of this process is the file 'AlignmentScoreHistogram.pdf'.

***********************************************************************************************

## USAGE:
python SequenceAlignment.py (name of reference txt file) (query txt file) [*match txt file*]

Square brackets indicate that the match file is optional- anchored Needleman-Wunsch will be run only if this file is supplied.
***********************************************************************************************
Ex: python SequenceAlignment.py TITIN_Human.fa TITIN_Mouse.fa TITIN_Match.txt

In this example the TITIN_Human becomes the reference sequence and TITIN_Mouse becomes the query. TITIN_Match is used to run anchored needleman-wunsch for the two sequences.

Also acceptable: python SequenceAlignment.py SAMPLEInput1.txt SAMPLEInput2.txt

This will 
