# Project contents:
	* Python source code
	* Sample input .txt files (sequence and match file samples) to show required format
	* Sample output .txt and .pdf files (produced from running the program on the sample files)
	* FASTA files for human and mouse TITIN protein sequences (TITIN is the largest known protein, ~30,000 amino acids in length)
	* Match file for the TITIN sequences
	* Output for aligning human and mouse TITIN sequences
	* This...

# GLOBAL SEQUENCE ALIGNMENT notes:
The task this accomplishes can be described as inserting gaps into two sequences of DNA/RNA or amino acids such that the resulting strings have an optimal similarity score. This task is important in genomics because the alignment and similarity score of two genes can indicate homologous sequences, suggesting an evolutionary relationship between the organisms each sequence came from. These scores can be further used to contruct phylogenetic trees for entire ecosystems.

To accomplish this task, the Needleman-Wunsch algorithm is implemented, as well as an anchored version. Anchored Needleman-Wunsch assumes some regions ('anchors') are known to match in both sequences, and the algorithm takes as input the start and end positions of each anchor as well as the two sequences to be aligned. The task of sequence alignment then becomes aligning the regions between anchors and building up the final alignment, saving time.

If desired, this program will also permute both sequences, perform alignment & scoring, and repeat 10,000 times. The resulting 1,000 scores are then made into a histogram and saved to a PDF file. This supports the claim that the unpermuted alignment is optimal.

## INPUT notes:
To run this program, the sequence files MUST be in the same folder as the program file 'SequenceAlignment.py', files CANNOT be opened by passing their path to the program. Input files must have the same format as the sample input files.

## OUTPUT notes:
Program always outputs a text file 'out.txt' containing the new sequences (with gaps inserted) and their alignment score. If a match file is passed as well, the program runs anchored Needleman-Wunsch. The program will also ask the user before repeatedly permuting and realigning the sequences, ultimately creating a histogram of alignment scores. If this last step is executed, the output of this process is the file 'AlignmentScoreHistogram.pdf'.

***********************************************************************************************

## USAGE:
python SequenceAlignment.py *name of reference txt file* *query txt file* [*match txt file*]

***********************************************************************************************

Ex: python SequenceAlignment.py SAMPLEInput1.txt SAMPLEInput2.txt SAMPLEMatch.txt
In this example the SAMPLEInput1 file becomes the reference sequence and SAMPLEInput2 becomes the query. SAMPLEMatch is used to run anchored needleman-wunsch for the two sequences.

Also acceptable: python SequenceAlignment.py SAMPLEInput1.txt SAMPLEInput.txt
In this example, the non-anchored needleman-wunsch algorithm will be run for the two given files, with SAMPLEInput1 and SAMPLEInput2 used as reference and query, respectively.