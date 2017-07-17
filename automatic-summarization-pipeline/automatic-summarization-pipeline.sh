#!/bin/sh

CLAS=TRUE
echo "   Classifying: $PRE"
SUMM=TRUE
echo "   Summarizing: $POS"

if [ "$CLAS" = "TRUE" ]; then
echo 'Classifying files...'
# Path for filtered sentences
INPUT_PATH=../preprocessing-files/features
# Path for classified sentences
OUTPUT_PATH=./classified
# Path for classification model
MODEL_PATH=.
# Classification model
MODEL=SVM_model
# Best feature
FEATURE=lemma_lemma_pos_pos
# TF name to be summarized
TF_NAME=MarA

python3.4 classify.py --inputPath $INPUT_PATH --inputFile $TF_NAME.$FEATURE.txt --outputPath $OUTPUT_PATH --outputFile $TF_NAME.txt --modelPath $MODEL_PATH --modelName $MODEL --inputTXTPath $INPUT_PATH --inputTXTFile $TF_NAME.word.txt
fi

if [ "$SUMM" = "TRUE" ]; then
echo 'Summarizing files...'

# Path for automatic summary
OUTPUT_PATH=../automatic-summary
# Path for classified sentences
INPUT_PATH=./classified
# File with classified setences
INPUT_FILE=$TF_NAME.txt

python3.4 makingAutomaticSummary.py --inputPath $INPUT_PATH --inputFile $INPUT_FILE --outputPath $OUTPUT_PATH --outputFile $TF_NAME-automatic-summary.txt --aspects DOM,RP --entityName $TF_NAME
fi
