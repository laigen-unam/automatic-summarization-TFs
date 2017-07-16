#!/bin/sh
echo 'Summarizing files...'

CORPUS_PATH=/home/cmendezc/AUTOMATIC_SUMMARIZATION_TFS/corpus_SummaryEvaluation
# Aspect sentence models
MODEL_PATH=/home/cmendezc/AUTOMATIC_SUMMARIZATION_TFS/trainingTest_NB_SVM/aspectSentence_freqWords

for GENE in ECK120012407_CytR ECK120011670_ArgR ECK120011412_MarA ECK120011394_FhlA ECK120012096_GntR
do
    ./classifyingParam_AspectSentenceModels_freqWords.sh $GENE $MODEL_PATH $CORPUS_PATH
done

# $2 MODEL_PATH
# $3 CORPUS_PATH

INPUT_PATH=$3/$1/features_freqWords
OUTPUT_PATH=$3/$1/classified_AspectSentence_freqWords

MODEL=l_l_p_p.SVM.SVD200.poly.vecTipoTFIDFStopFalseStriNoneNgrI1NgrF2TruncFalseLowerFalse.LOGNone
FEATURE=lemma_lemma_pos_pos
python3.4 classify.py --inputPath $INPUT_PATH --inputFile $1.$FEATURE.txt --outputPath $OUTPUT_PATH --outputFile $MODEL.txt --modelPath $2 --modelName $MODEL --inputTXTPath $INPUT_PATH --inputTXTFile $1.word.txt

##############3

OUTPUT_PATH=/home/cmendezc/AUTOMATIC_SUMMARIZATION_TFS/classifying_TFSentences/all_ROUGE_Evaluation/peers
CORPUS_PATH=/home/cmendezc/AUTOMATIC_SUMMARIZATION_TFS/corpus_SummaryEvaluation

for GENE in ECK120012407_CytR ECK120011670_ArgR ECK120011412_MarA ECK120011394_FhlA ECK120012096_GntR
do
    ./makingSummaryParam_AspectSentenceModels_freqWords.sh $GENE $OUTPUT_PATH $CORPUS_PATH
done


# Classifying gene %1...
# %2 OUTPUT_PATH
# %3 CORPUS_PATH

STRING=$1
GENE=${STRING#*_}
echo $GENE

INPUT_PATH=$3/$1/classified_AspectSentence_freqWords
OUTPUT_PATH=$2

INPUT_FILE=l_l_p_p.SVM.SVD200.poly.vecTipoTFIDFStopFalseStriNoneNgrI1NgrF2TruncFalseLowerFalse.LOGNone.txt
python3.4 makingAutomaticSummary.py --inputPath $INPUT_PATH --inputFile $INPUT_FILE --outputPath $OUTPUT_PATH --outputFile $1_automaticSummary_aspectSentence_freqWords.txt --aspects DOM,RP --entityName $GENE

