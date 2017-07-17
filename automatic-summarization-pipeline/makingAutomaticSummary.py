# -*- coding: UTF-8 -*-
import re
from optparse import OptionParser
import os
import sys
from time import time

__author__ = 'CMendezC'

# Objective: Take files with classified sentences into aspects
#   and make summary, one file per aspect of interest.
# SUMMARY = concatenation of sentences

# Parameters:
#   1) --inputPath      Path to read files.
#   2) --inputFile      File to read.
#   3) --outputPath     Path to write output files.
#   2) --outputFile      File to write.
#   4) --aspects        Aspects of interest to make summary
#   5) --entityName     Entity name to output file name

# Ouput:
#   1) Summary files created. Name of entity and aspect are concatenated

# Rob
# python makingAutomaticSummary.py
# --inputPath C:\Users\cmendezc\Documents\GENOMICAS\AUTOMATIC_SUMMARIZATION_TFS\corpus\TF_PMIDs_TXT_ECK120011190_Rob\manualSummary\paso
# --inputFile aspects_ECK120011190_Rob.l_l_p_p.SVM.None100.linear.vecTipoCOUNTStopFalseStriNoneNgrI1NgrF2TruncFalseLowerFalse.LOGNone.txt
# --outputPath C:\Users\cmendezc\Documents\GENOMICAS\AUTOMATIC_SUMMARIZATION_TFS\corpus\TF_PMIDs_TXT_ECK120011190_Rob\manualSummary\aspects
# --outputFile automaticSummary_E01_ECK120011190_Rob.txt
# --aspects RP,DOM
# --entityName Rob

###########################################################
#                       MAIN PROGRAM                      #
###########################################################

if __name__ == "__main__":
    # Parameter definition
    parser = OptionParser()
    parser.add_option("--inputPath", dest="inputPath",
                      help="Path to read files", metavar="PATH")
    parser.add_option("--inputFile", dest="inputFile",
                      help="Input file", metavar="FILE")
    parser.add_option("--outputPath", dest="outputPath",
                      help="Path to write output file", metavar="PATH")
    parser.add_option("--outputFile", dest="outputFile",
                      help="Output file", metavar="FILE")
    parser.add_option("--aspects", dest="aspects",
                      help="Aspect sentences to extract", metavar="TEXT,TEXT")
    parser.add_option("--entityName", dest="entityName",
                      help="Entity name to concatenate to file name", metavar="FILE")

    (options, args) = parser.parse_args()
    if len(args) > 0:
        parser.error("None parameters indicated.")
        sys.exit(1)

    # Printing parameter values
    print('-------------------------------- PARAMETERS --------------------------------')
    print("Input path: " + str(options.inputPath))
    print("Input file: " + str(options.inputFile))
    print("Output path: " + str(options.outputPath))
    print("Output file: " + str(options.outputFile))
    print("Aspect sentences to extract: " + str(options.aspects))
    print("Entity name to concatenate to file name: " + str(options.entityName))

    t0 = time()

    listAspects = list(options.aspects.split(','))
    print("Features list: " + str(listAspects))

    listSentences = []
    hashSummaries = {}

    with open(os.path.join(options.inputPath, options.inputFile), "r", encoding="utf-8", errors="replace") as sFile:
        for line in sFile:
            listLine = line.rstrip('\n').split('\t')
            c = listLine[3]
            # print(c)
            s = listLine[1]
            # print(s)
            if c in listAspects:
                print('class: ' + c)
                if c in hashSummaries:
                    hashSummaries[c] += s + '\n'
                else:
                    hashSummaries[c] = s + '\n'

    # One file all classes
    with open(os.path.join(options.outputPath, options.outputFile), "w", encoding="utf-8") as oFile:
        for c in hashSummaries.keys():
            oFile.write(hashSummaries[c])
    # One file per class
    # for c in hashSummaries.keys():
    #     with open(os.path.join(options.outputPath, options.outputFile.replace('.txt', '_' + c + '.txt')), "w", encoding="utf-8") as oFile:
    #             oFile.write(hashSummaries[c])

    print("Files processed in: %fs" % (time() - t0))