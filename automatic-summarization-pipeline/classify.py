# -*- encoding: utf-8 -*-

import os
from time import time
from optparse import OptionParser
from nltk import word_tokenize
import sys
from scipy.sparse import csr_matrix
from sklearn.externals import joblib
from sklearn.svm import SVC
import scipy.stats
from definingVectorizer import definingVectorizer
from sklearn import model_selection

__author__ = 'CMendezC'

# Objetivo: classify text files into classes by using trained SVM model and vectorizer.
#   Model and vectorizer were trained with trainingTesting.py

# Parameters
#   1) --inputPath Path to read TXT files to classify.
#   2) --inputFile File to read text to classify (one per line). If parameter --fromFile is True.
#   3) --outputPath Path to place classified TXT files.
#   4) --outputFile Output file name to write classified text. If parameter --toFile is True
#   5) --modelPath Parent path to read trained model, vectorizer, and dimensionality reduction.
#   7) --modelName Name of model and vectorizer to load.
#   8) --inputTXTPath   Path to read TXT file equivalent to file with features extracted.
#   9) --inputTXTFile   TXT file equivalent to file with features extracted.
#   10) --onlyClass Name of class to deliver files or write into a file
#   11) --clasePos Clase positiva para clasificación
#   12) --claseNeg Clase negativa para clasificación

# Ouput:
#   1) A file with classified sentences (one per line), with class.

# Execution:
# ASPECTS
# modelName l_l_p_p.SVM.SVD300.rbf.vecTipoCOUNTStopFalseStriNoneNgrI1NgrF1TruncFalseLowerFalse.LOGNone
# C:\Anaconda3\python classify.py --inputPath C:\Users\cmendezc\Documents\GENOMICAS\AUTOMATIC_SUMMARIZATION_TFS\corpus\TF_PMIDs_TXT_ECK120012096_GntR --inputFile ECK120012096_GntR.lemma_lemma_pos_pos.txt --outputPath C:\Users\cmendezc\Documents\GENOMICAS\AUTOMATIC_SUMMARIZATION_TFS\corpus\TF_PMIDs_TXT_ECK120012096_GntR --outputFile ECK120012096_GntR.lemma_lemma_pos_pos.classified.txt --modelPath C:\Users\cmendezc\Documents\GENOMICAS\AUTOMATIC_SUMMARIZATION_TFS\corpus\aspectClassificationDatasets\aspects_TrainingTest_RP_DOM_20160723 --modelName l_l_p_p.SVM.SVD300.rbf.vecTipoCOUNTStopFalseStriNoneNgrI1NgrF1TruncFalseLowerFalse.LOGNone --inputTXTPath C:\Users\cmendezc\Documents\GENOMICAS\AUTOMATIC_SUMMARIZATION_TFS\corpus\TF_PMIDs_TXT_ECK120012096_GntR --inputTXTFile ECK120012096_GntR.word.txt
# modelName lemma.SVM.None100.rbf.vecTipoCOUNTStopFalseStriNoneNgrI1NgrF2TruncFalseLowerFalse.LOGNone
# C:\Anaconda3\python classify.py --inputPath C:\Users\cmendezc\Documents\GENOMICAS\AUTOMATIC_SUMMARIZATION_TFS\corpus\TF_PMIDs_TXT_ECK120012096_GntR --inputFile ECK120012096_GntR.lemma.txt --outputPath C:\Users\cmendezc\Documents\GENOMICAS\AUTOMATIC_SUMMARIZATION_TFS\corpus\TF_PMIDs_TXT_ECK120012096_GntR --outputFile ECK120012096_GntR.lemma.classified.txt --modelPath C:\Users\cmendezc\Documents\GENOMICAS\AUTOMATIC_SUMMARIZATION_TFS\corpus\aspectClassificationDatasets\aspects_TrainingTest_RP_DOM_20160723 --modelName lemma.SVM.None100.rbf.vecTipoCOUNTStopFalseStriNoneNgrI1NgrF2TruncFalseLowerFalse.LOGNone --inputTXTPath C:\Users\cmendezc\Documents\GENOMICAS\AUTOMATIC_SUMMARIZATION_TFS\corpus\TF_PMIDs_TXT_ECK120012096_GntR --inputTXTFile ECK120012096_GntR.word.txt

# SENTENCES
# modelName l_l_p_p.SVM.SVD300.rbf.vecTipoTFIDFStopFalseStriNoneNgrI1NgrF3TruncFalseLowerFalse.LOGNone
# python3.4 classify.py
# --inputPath /home/cmendezc/O9-NLP-TFs/corpus/TF_PMIDs_TXT_ECK120012096_GntR
# --inputFile ECK120012096_GntR.lemma_lemma_pos_pos.txt
# --outputPath /home/cmendezc/O9-NLP-TFs/corpus/TF_PMIDs_TXT_ECK120012096_GntR
# --outputFile ECK120012096_GntR.lemma_lemma_pos_pos.classified.txt
# --modelPath /home/cmendezc/O9-NLP-TFs/corpus/aspectClassificationDatasets/sentences_TrainingTest_RP_DOM_20160725
# --modelName l_l_p_p.SVM.SVD300.rbf.vecTipoTFIDFStopFalseStriNoneNgrI1NgrF3TruncFalseLowerFalse.LOGNone
# --inputTXTPath /home/cmendezc/O9-NLP-TFs/corpus/TF_PMIDs_TXT_ECK120012096_GntR
# --inputTXTFile ECK120012096_GntR.word.txt
# C:\Anaconda3\python classify.py
# --inputPath C:\Users\cmendezc\Documents\GENOMICAS\AUTOMATIC_SUMMARIZATION_TFS\corpus\TF_PMIDs_TXT_ECK120012096_GntR
# --inputFile ECK120012096_GntR.lemma_lemma_pos_pos.txt
# --outputPath C:\Users\cmendezc\Documents\GENOMICAS\AUTOMATIC_SUMMARIZATION_TFS\corpus\TF_PMIDs_TXT_ECK120012096_GntR
# --outputFile ECK120012096_GntR.lemma_lemma_pos_pos.classified.txt
# --modelPath C:\Users\cmendezc\Documents\GENOMICAS\AUTOMATIC_SUMMARIZATION_TFS\corpus\aspectClassificationDatasets\sentences_TrainingTest_RP_DOM_20160725
# --modelName l_l_p_p.SVM.SVD300.rbf.vecTipoTFIDFStopFalseStriNoneNgrI1NgrF3TruncFalseLowerFalse.LOGNone
# --inputTXTPath C:\Users\cmendezc\Documents\GENOMICAS\AUTOMATIC_SUMMARIZATION_TFS\corpus\TF_PMIDs_TXT_ECK120012096_GntR
# --inputTXTFile ECK120012096_GntR.word.txt

# lemma.SVM.SVD200.rbf.vecTipoTFIDFStopFalseStriNoneNgrI1NgrF1TruncFalseLowerFalse.LOGNone

# python3.4 classify.py --inputPath /home/cmendezc/O9-NLP-TFs/corpus/TF_PMIDs_TXT_ECK120012096_GntR
# --inputFile ECK120012096_GntR.lemma_lemma_pos_pos.txt
# --outputPath /home/cmendezc/O9-NLP-TFs/corpus/TF_PMIDs_TXT_ECK120012096_GntR
# --outputFile ECK120012096_GntR.lemma_lemma_pos_pos.classified.txt
# --modelPath /home/cmendezc/O9-NLP-TFs/corpus/aspectClassificationDatasets/sentences_TrainingTest_RP_DOM_20160725
# --modelName lemma.SVM.SVD200.rbf.vecTipoTFIDFStopFalseStriNoneNgrI1NgrF1TruncFalseLowerFalse.LOGNone
# --inputTXTPath /home/cmendezc/O9-NLP-TFs/corpus/TF_PMIDs_TXT_ECK120012096_GntR
# --inputTXTFile ECK120012096_GntR.word.txt

# ASPECTS - BEST MODELS
# classifyingGenes_Aspects.bat

# SENTENCES - BEST MODELS
# classifyingGenes_BothModels.bat (classifyingParam_AspectSentenceModels.bat)

class truncar(object):
    def __call__(self, doc):
        return [ocur[:6] for ocur in word_tokenize(doc)]

###########################################################
#                       MAIN PROGRAM                      #
###########################################################

if __name__ == "__main__":
    # Parameter definition
    parser = OptionParser()
    parser.add_option("--inputPath", dest="inputPath",
                      help="Path to read file with features extracted to classify", metavar="PATH")
    parser.add_option("--inputFile", dest="inputFile",
                      help="File to read text to classify (one per line)", metavar="FILE")
    parser.add_option("--outputPath", dest="outputPath",
                      help="Path to place classified text", metavar="PATH")
    parser.add_option("--outputFile", dest="outputFile",
                      help="Output file name to write classified text", metavar="FILE")
    parser.add_option("--modelPath", dest="modelPath",
                      help="Path to read trained model", metavar="PATH")
    parser.add_option("--modelName", dest="modelName",
                      help="Name of model and vectorizer to load", metavar="NAME")
    parser.add_option("--inputTXTPath", dest="inputTXTPath",
                      help="Path to read TXT file equivalent to file with features extracted", metavar="PATH")
    parser.add_option("--inputTXTFile", dest="inputTXTFile",
                      help="TXT file equivalent to file with features extracted", metavar="FILE")
    parser.add_option("--onlyClass", dest="onlyClass",
                      help="Name of class to deliver files or write into a file", metavar="NAME")
    # Clase positiva para clasificación
    parser.add_option("--clasePos", dest="clasePos",
                      help="Clase positiva del corpus", metavar="CLAS")
    # Clase negativa para clasificación
    parser.add_option("--claseNeg", dest="claseNeg",
                      help="Clase negativa del corpus", metavar="CLAS")

    (options, args) = parser.parse_args()
    if len(args) > 0:
        parser.error("None parameters indicated.")
        sys.exit(1)

    # Printing parameter values
    print('-------------------------------- PARAMETERS --------------------------------')
    print("Path to read file with features extracted to classify: " + str(options.inputPath))
    print("File to read text to classify (one per line): " + str(options.inputFile))
    print("Path to place classified TXT file: " + str(options.outputPath))
    print("Output file name to write classified text: " + str(options.outputFile))
    print("Path to read trained model, vectorizer, and dimensionality reduction: " + str(options.modelPath))
    print("Name of model, vectorizer, and dimensionality reduction to load: " + str(options.modelName))
    print("Path to read TXT file equivalent to file with features extracted: " + str(options.inputTXTPath))
    print("TXT file equivalent to file with features extracted: " + str(options.inputTXTPath))
    print("Name of class to deliver files or write into a file: " + str(options.onlyClass))
    print("Positive class: " + str(options.claseNeg))
    print("Negative class: " + str(options.clasePos))

    t0 = time()

    fileCount = 0
    listWordTexts = []
    listFeatureTexts = []
    filenameList = []
    listIndex = []

    with open(os.path.join(options.inputPath, options.inputFile), 'r', encoding='utf8', errors='replace') as iFile:
    #with open(os.path.join(options.inputPath, options.inputFile), 'r') as iFile:
        for line in iFile.readlines():
            listLine = line.strip('\n').split('\t')
            listIndex.append(listLine[0] + '_' + listLine[1])
            listFeatureTexts.append(listLine[2])

    with open(os.path.join(options.inputTXTPath, options.inputTXTFile), 'r', encoding='utf8', errors='replace') as iFile:
    #with open(os.path.join(options.inputTXTPath, options.inputTXTFile), 'r') as iFile:
        for line in iFile.readlines():
            listLine = line.strip('\n').split('\t')
            listWordTexts.append(listLine[2])

    print("Classifying texts...")
    print("   Loading model and vectorizer: " + options.modelName)
    if options.modelName.find('.SVM.'):
        classifier = SVC()
    classifier = joblib.load(os.path.join(options.modelPath, 'models', options.modelName + '.mod'), mmap_mode=None)
    vectorizer = joblib.load(os.path.join(options.modelPath, 'vectorizers', options.modelName + '.vec'))

    matrix = csr_matrix(vectorizer.transform(listFeatureTexts), dtype='double')
    print("   matrix.shape " + str(matrix.shape))

    # USING DIMENSIONALITY REDUCTION
    posSVD = options.modelName.find('SVD')
    if posSVD > -1:
        t1 = time()
        print('       Performing dimensionality reduction...')
        #reduc = TruncatedSVD(n_components=300, random_state=42)
        reduc = joblib.load(os.path.join(options.modelPath, 'reductions', options.modelName + '.red'))
        matrix = reduc.transform(matrix)

        #reduction = 'SVD'
        #components = int(options.modelName[posSVD + 3:posSVD + 3 + 3])
        #print('Components: ' + str(components))
        #print('       Performing dimensionality reduction...', reduction)
        #if reduction == 'SVD':
        #    reduc = TruncatedSVD(n_components=components, random_state=42)
        #    matrix = reduc.fit_transform(matrix)
        # elif options.reduction == 'SVC':
        #    reduc = LinearSVC(penalty="l1", dual=False, tol=1e-3)
        #    matrixTraining = reduc.fit_transform(matrixTraining)

        print("          Performing dimensionality reduction done in: %fs" % (time() - t1))
        print('     matrixTraining.shape: ', matrix.shape)

    # Classify corpus list
    listPredictedClasses = classifier.predict(matrix)

    print("   Predicted class list length: " + str(len(listPredictedClasses)))

    with open(os.path.join(options.outputPath, options.outputFile), "w", encoding="utf-8") as oFile:
        oFile.write('IDX\tWORD_TEXT\tFEATURE_TEXT\tPREDICTED_CLASS\n')
        for idx, wt, ft, pc in zip(listIndex, listWordTexts, listFeatureTexts, listPredictedClasses):
            oFile.write(idx + '\t'+ wt + '\t' + ft + '\t' + pc + '\n')

    print("Texts classified in : %fs" % (time() - t0))
