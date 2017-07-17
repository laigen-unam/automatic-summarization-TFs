#!/bin/sh
echo 'Preprocessing files...'
# Path for original text articles
ORIGINAL_CORPUS_PATH=../preprocessing-files/original
# Path with directories employed to save preprocessing
PREPROCESSING_PATH=../preprocessing-files
# Path for term lists
TERM_PATH=../termLists
# Path for Stanford POS Tagger
STANFORD_POSTAGGER_PATH=/home/cmendezc/STANFORD_POSTAGGER/stanford-postagger-2015-12-09
# Path for BioLemmatizer
BIO_LEMMATIZER_PATH=/home/cmendezc/BIO_LEMMATIZER
# TF name to be summarized
TF_NAME=MarA

PRE=TRUE
echo "   Preprocessing: $PRE"
POS=TRUE
echo "   POS Tagging: $POS"
LEMMA=TRUE
echo "   Lemmatization: $LEMMA"
TERM=TRUE
echo "   Terminological tagging: $TERM"
TRANS=TRUE
echo "   Transformation: $TRANS"
FEAT=TRUE
echo "   Feature extraction: $FEAT"

if [ "$PRE" = "TRUE" ]; then
echo "Preprocessing..."
INPUT_PATH=$ORIGINAL_CORPUS_PATH
OUTPUT_PATH=$PREPROCESSING_PATH/preprocessed
python3.4 preprocessingTermDetection.py --inputPath $INPUT_PATH --outputPath $OUTPUT_PATH --termDetection --termPath $TERM_PATH --termFiles termFilesLength_TFSummarization.json > outputPreprocessing.txt
fi

if [ "$POS" = "TRUE" ]; then
echo "POS Tagging..."
INPUT_PATH=$PREPROCESSING_PATH/preprocessed
OUTPUT_PATH=$PREPROCESSING_PATH/pos
python3.4 posTaggingStanford.py --inputPath $INPUT_PATH --outputPath $OUTPUT_PATH --taggerPath $STANFORD_POSTAGGER_PATH --biolemmatizer > outputPOST.txt
fi

if [ "$LEMMA" = "TRUE" ]; then
echo "Lemmatization..."
INPUT_PATH=$PREPROCESSING_PATH/pos
OUTPUT_PATH=$PREPROCESSING_PATH/lemma
python3.4 biolemmatizing.py --inputPath $INPUT_PATH --outputPath $OUTPUT_PATH --biolemmatizerPath $BIO_LEMMATIZER_PATH  > outputLemma.txt
fi

if [ "$TERM" = "TRUE" ]; then
echo "Terminological tagging..."
INPUT_PATH=$PREPROCESSING_PATH/lemma
OUTPUT_PATH=$PREPROCESSING_PATH/term
python3.4 biologicalTermTagging.py --inputPath $INPUT_PATH --outputPath $OUTPUT_PATH --termPath $TERM_PATH --termFiles termFilesTag_TFSummarization_FreqWords.json > outputTerm.txt
fi

if [ "$TRANS" = "TRUE" ]; then
echo "Transformation..."
INPUT_PATH=$PREPROCESSING_PATH/term
OUTPUT_PATH=$PREPROCESSING_PATH/transformed
python3.4 transforming.py --inputPath $INPUT_PATH --outputPath $OUTPUT_PATH --minWordsInLine 5 > outputTransformation.txt
fi

if [ "$FEAT" = "TRUE" ]; then
echo "Feature extraction..."
INPUT_PATH=$PREPROCESSING_PATH/transformed
OUTPUT_PATH=$PREPROCESSING_PATH/features
python3.4 featureExtractionPapers.py --inputPath $INPUT_PATH --outputPath $OUTPUT_PATH --feature lemma_lemma_pos_pos,word --outputFile $TF_NAME.txt --entityName $TF_NAME --concatenate > outputFeatureExtraction.txt
fi