# -*- coding: UTF-8 -*-
import re
from optparse import OptionParser
import os
import sys
from time import time

__author__ = 'CMendezC'

# Objective: Take transformed files with format word|lemma|pos,
#   for example: Multiple|multiple|JJ genetic|genetic|JJ variants|variant|NNS have|have|VBP
#   and create files with a different representation such as:
#   a) word = word
#   b) lemma = lemma
#   c) pos = pos
#   d) word_pos = word_pos word_pos
#   e) lemma_pos = lemma_pos lemma_pos

# Parameters:
#   1) --inputPath      Path to read files.
#   2) --outputPath     Path to write feature extraction files. File names are concatenated with feature name.
#   3) --feature        Type of feature to extract and create file: word, lemma, etc
#   4) --outputFile     File to concatenate all read files
#   5) --entityName     Entity names to filter sentences, names separated by -

# Ouput:
#   1) Files created. Name of feature is concatenated

###########################################################
#                       MAIN PROGRAM                      #
###########################################################

if __name__ == "__main__":
    # Parameter definition
    parser = OptionParser()
    parser.add_option("--inputPath", dest="inputPath",
                      help="Path to read files", metavar="PATH")
    parser.add_option("--outputPath", dest="outputPath",
                      help="Path to write feature extraction files, program is going to use --feature parameter to concatenate to file name.", metavar="PATH")
    parser.add_option("--features", dest="features",
                      help="Types of features to extract and create file: word,lemma,word_pos_word_pos,lemma_pos_lemma_pos,pos,word_word_pos_pos,lemma_lemma_pos_pos", metavar="TEXT,TEXT")
    parser.add_option("--outputFile", dest="outputFile",
                      help="File to concatenate all read files", metavar="FILE")
    parser.add_option("--entityName", dest="entityName",
                      help="Entity name to filter sentences", metavar="FILE")
    parser.add_option("--concatenate", default=False,
                      action="store_true", dest="concatenate",
                      help="Concatenate all text into one file")

    (options, args) = parser.parse_args()
    if len(args) > 0:
        parser.error("None parameters indicated.")
        sys.exit(1)

    # Printing parameter values
    print('-------------------------------- PARAMETERS --------------------------------')
    print("Path to read files: " + str(options.inputPath))
    print("Path to write feature extraction files: " + str(options.outputPath))
    print("Types of feature to extract: " + str(options.features))
    print("Output file: " + str(options.outputFile))
    print("Entity name to filter sentences: " + str(options.entityName))
    print("Concatenate all text into one file?: " + str(options.concatenate))

    filesProcessed = 0
    t0 = time()

    featuresList = list(options.features.split(','))
    print("Features list: " + str(featuresList))

    if options.entityName is not None:
        # Creating regex for name entities as synonyms
        listEntities = options.entityName.split('-')
        if len(listEntities) == 1:
            entityPattern = options.entityName + '\|'
        else:
            entityPattern = '('
            for ent in listEntities:
                entityPattern += ent + '\|' + '|'
            entityPattern = entityPattern[:len(entityPattern)-1]
            entityPattern += ')'
        print('Pattern for entity names to filter: ' + entityPattern)

    for path, dirs, files in os.walk(options.inputPath):
        for feature in featuresList:
            print("Extracting feature: " + feature)
            allText = ''
            for file in files:
                fileName = file[:file.find('.')]
                # print('     Filename: ' + fileName)
                with open(os.path.join(options.inputPath, file), mode="r", encoding="utf-8", errors="replace") as tFile:
                    print("   Extracting features from file..." + str(file))
                    lines = tFile.readlines()
                    filesProcessed += 1
                    with open(os.path.join(options.outputPath, file.replace('tra.txt', feature + '.txt')), "w", encoding="utf-8") as featFile:
                        lineNumber = 1
                        for line in lines:
                            wordLine = ''
                            lemmaLine = ''
                            posLine = ''
                            # Filtering by entityName
                            if options.entityName is not None:
                                # regexEntityName = re.compile(options.entityName + '\|')
                                regexEntityName = re.compile(entityPattern)
                                if regexEntityName.search(line) is None:
                                    continue
                                else:
                                    pass
                                    # print("     TF line: " + str(line.encode(encoding='UTF-8', errors='replace')))
                            for tok in line.split():
                                tokList = tok.split("|")
                                if len(tokList) < 3:
                                    print('Bad token:' + tok)
                                if feature == "word":
                                    wordLine += tokList[0] + " "
                                if feature == "lemma":
                                    lemmaLine += tokList[1] + " "
                                if feature == "pos":
                                    posLine += tokList[2] + " "
                                if feature == "word_pos_word_pos":
                                    wordLine += tokList[0] + "_" + tokList[2] + " "
                                if feature == "lemma_pos_lemma_pos":
                                    lemmaLine += tokList[1] + "_" + tokList[2] + " "
                                if feature == "word_word_pos_pos":
                                    wordLine += tokList[0] + " "
                                    posLine += tokList[2] + " "
                                if feature == "lemma_lemma_pos_pos":
                                    lemmaLine += tokList[1] + " "
                                    posLine += tokList[2] + " "
                            if feature == "word":
                                featFile.write(wordLine.strip() + '\n')
                                if options.concatenate:
                                    allText += fileName + '\t' + str(lineNumber) + '\t' + wordLine.strip() + '\n'
                            if feature == "lemma":
                                featFile.write(lemmaLine.strip() + '\n')
                                if options.concatenate:
                                    allText += fileName + '\t' + str(lineNumber) + '\t' + lemmaLine.strip() + '\n'
                            if feature == "pos":
                                featFile.write(posLine.strip() + '\n')
                                if options.concatenate:
                                    allText += fileName + '\t' + str(lineNumber) + '\t' + posLine.strip() + '\n'
                            if feature == "word_pos_word_pos":
                                featFile.write(wordLine.strip() + '\n')
                                if options.concatenate:
                                    allText += fileName + '\t' + str(lineNumber) + '\t' + wordLine.strip() + '\n'
                            if feature == "lemma_pos_lemma_pos":
                                featFile.write(lemmaLine.strip() + '\n')
                                if options.concatenate:
                                    allText += fileName + '\t' + str(lineNumber) + '\t' + lemmaLine.strip() + '\n'
                            if feature == "word_word_pos_pos":
                                featFile.write(wordLine + posLine.strip() + '\n')
                                if options.concatenate:
                                    allText += fileName + '\t' + str(lineNumber) + '\t' + wordLine + posLine.strip() + '\n'
                            if feature == "lemma_lemma_pos_pos":
                                featFile.write(lemmaLine + posLine.strip() + '\n')
                                if options.concatenate:
                                    allText += fileName + '\t' + str(lineNumber) + '\t' + lemmaLine + posLine.strip() + '\n'
                            lineNumber += 1
            if options.concatenate:
                with open(os.path.join(options.outputPath, options.outputFile.replace('.txt', '.' + feature + '.txt')), "w", encoding="utf-8") as oFile:
                    oFile.write(allText)

    print("Files processed: " + str(filesProcessed))