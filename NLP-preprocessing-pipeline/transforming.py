# -*- coding: UTF-8 -*-
import re
from optparse import OptionParser
import os
import sys
from time import time

__author__ = 'CMendezC'

# Objective: Transforming BIOLemmatized files:
#   1) Transformed files
#   2) Text files to extract aspects

# Parameters:
#   1) --inputPath Path to read input files.
#   2) --outputPath Path to place output files.
#   3) --textPath Path to place output files.
#   4) --minWordsInLine Minimum length sentence in number of words
#   5) --classes Classes to indicate final of sentence when line contains: PMID\tNUMSENT\tSENT\tCLASS

# Output:
#   1) transformed files
#   2) text files

def length(listWords):
    regexWord = re.compile('[a-zA-Z]')
    words = 0
    chars = 0
    for word in listWords:
        listTemp = word.split('|')
        if regexWord.search(listTemp[1]) is not None:
            words += 1
        chars += len(listTemp[0])
    return words, chars

###########################################################
#                       MAIN PROGRAM                      #
###########################################################

if __name__ == "__main__":
    # Parameter definition
    parser = OptionParser()
    parser.add_option("-i", "--inputPath", dest="inputPath",
                      help="Path to read input files", metavar="PATH")
    parser.add_option("-o", "--outputPath", dest="outputPath",
                      help="Path to place transformed files", metavar="PATH")
    parser.add_option("--minWordsInLine", type="int", dest="minWordsInLine",
                      help="Minimum length sentence in number of words", metavar="NUM")
    parser.add_option("--classes", dest="classes",
                      help="Classes to indicate final of sentence when line contains: PMID-NUMSENT-SENT-CLASS", metavar="CLASS,CLASS")

    (options, args) = parser.parse_args()

    if len(args) > 0:
        parser.error("None parameters indicated.")
        sys.exit(1)

    # Printing parameter values
    print('-------------------------------- PARAMETERS --------------------------------')
    print("Path to read input files: " + str(options.inputPath))
    print("Path to place transformed files: " + str(options.outputPath))
    print("Minimum length sentence in number of words: " + str(options.minWordsInLine))
    print("Classes to indicate final of sentence: " + str(options.classes))

    # We realized that POS tags from Biolemmatizer are very specific, therefore we decided to use Standford tags
    bioPOST = True
    filesProcessed = 0
    # minWordsInLine = 3
    if not options.classes is None:
        listClasses = options.classes.split(',')
    t0 = time()
    print("Transforming files...")
    # Walk directory to read files
    for path, dirs, files in os.walk(options.inputPath):
        # For each file in dir
        for file in files:
            print("   Transforming file..." + str(file))
            #TrpR	NN	TrpR NN PennPOS
            # ,	,	, , NUPOS
            # tryptophan	NN	tryptophan NN PennPOS
            listLine1 = []
            listLine2 = []
            text = ''
            lemma = ''
            pos = ''
            textTransformed = ''
            textText = ''
            with open(os.path.join(path, file), "r", encoding="utf-8", errors="replace") as iFile:
                # Create output file to write
                with open(os.path.join(options.outputPath, file.replace('term.txt', 'tra.txt')), "w", encoding="utf-8") as transformedFile:
                    for line in iFile:
                        if line == '\n':
                            if options.classes is None:
                                if length(textTransformed.split())[0] > options.minWordsInLine and length(textTransformed.split())[1] <= 1000:
                                    transformedFile.write(textTransformed + '\n')
                                textTransformed = ''
                                textText = ''
                            else:
                                continue
                        else:
                            line = line.strip('\n')
                            #print('Line ' + str(line.encode(encoding='UTF-8', errors='replace')))
                            listLine1 = line.split('\t')
                            if len(listLine1) != 3:
                                continue
                            text = listLine1[0]
                            # Replacing an strange space character
                            text = text.replace(' ', '-')
                            listLine2 = listLine1[2].split(' ')
                            lemma = listLine2[0]
                            # Replacing an estrange space character
                            lemma = lemma.replace(' ', '-')
                            if bioPOST:
                                pos = listLine2[1]
                                #print('Line ' + str(line.encode(encoding='UTF-8', errors='replace')))
                            else:
                                pos = listLine1[1]
                            textText = textText + text + ' '
                            textTransformed = textTransformed + text + '|' + lemma + '|' + pos + ' '
                            # RI+GC	NN	RI+GC NN PennPOS
                            if not options.classes is None:
                                if text in listClasses:
                                    # if length(textTransformed.split()) > options.minWordsInLine:
                                    if length(textTransformed.split())[0] > options.minWordsInLine and length(textTransformed.split())[1] <= 1000:
                                        transformedFile.write(textTransformed + '\n')
                                        # print(textTransformed)
                                    textTransformed = ''
                                    textText = ''
            filesProcessed += 1

    print()
    print("Files processed: " + str(filesProcessed))
    print("In: %fs" % (time() - t0))
