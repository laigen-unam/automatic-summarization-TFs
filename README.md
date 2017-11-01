# Automatic summarization of transcription factor properties

In the BioNLP group of the Computational Genomics Program (Center for Genomic Sciences, Mexico), we conduct research on automatic text summarization for helping the biocuration process of RegulonDB (http://regulondb.ccg.unam.mx/).

RegulonDB is a database dedicated to the transcriptional regulation of *Escherichia coli K-12*. This database contains a set of summaries about several properties of TFs. These summaries are also found in EcoCyc (https://ecocyc.org/). These summaries are written manually by using several scientific articles.

We have proposed an initial approach for the automatic generation of these summaries. In this initial approach, we generate summaries only about two properties of TFs:
1.	The biological processes in which the regulated genes are involved
2.	The number, name, and size of the structural domains constituting the TF

The automatic summaries are made by the concatenation of the automatically classified sentences from scientific articles by an SVM classifier. The evaluation of these initial automatic summaries indicated that they carried part of the relevant information included in the manual summaries.
 
This repository provides a pipeline for generating these initial automatic summaries.

# Reference
Méndez-Cruz, C.-F., Gama-Castro, S., Mejía-Almonte, C., Castillo-Villalba, M.-P., Muñiz-Rascado, L.-J. (2017). **First steps in automatic summarization of transcription factor properties for RegulonDB: classification of sentences about structural domains and regulated processes**. *Database*, Volume 2017, 1 January 2017, bax070, https://doi.org/10.1093/database/bax070.

# Input
You must place input files of the article collection within `preprocessing_pipeline/original/` directory. Input files must be raw text files. Extension *.txt is mandatory.

# NLP preprocessing pipeline
The first step is preprocessing the input files with the `NLP-preprocessing-pipeline/NLP-preprocessing-pipeline.sh` shell script. This step must be performed only once for the same article collection.

## Preprocessing directory
Our pipeline utilizes the `preprocessing-files` directory to save temporary files for each preprocessing task. These files could be removed after the NLP preprocessing has finished, except those for the `features` directory. These files are used for the automatic classification task.

## Term list directory
Several term lists are employed. These lists are on the term list directory `termLists`.

## Configure
You must indicate the path for the input texts directory (`ORIGINAL_CORPUS_PATH`), the preprocessing directory (`PREPROCESSING_PATH`), the term list directory (`TERM_PATH`), the Stanford POS Tagger directory (`STANFORD_POSTAGGER_PATH`), the BioLemmatizer directory (`BIO_LEMMATIZER_PATH`), and the name of the TF for summarization (`TF_NAME`). 
```shell
    ORIGINAL_CORPUS_PATH=../preprocessing-files/original
    PREPROCESSING_PATH=../preprocessing-files
    TERM_PATH=../termLists
    STANFORD_POSTAGGER_PATH=/home/cmendezc/STANFORD_POSTAGGER/stanford-postagger-2015-12-09
    BIO_LEMMATIZER_PATH=/home/cmendezc/BIO_LEMMATIZER
    TF_NAME=MarA
```

You must have installed Stanford POS Tagger and BioLemmatizer within your computer. They are not included within this repository, see following references for obtaining these programs:
- Toutanova, K., Klein, D., Manning, C. and Singer, Y. (2003) Feature-rich part-of-speech tagging with a cyclic dependency network. In Proceedings of the HLT-NAACL, pp. 252-259.
- https://nlp.stanford.edu/software/tagger.shtml
- Liu, H., Christiansen, T., Baumgartner, W. A., Jr., and Verspoor, K. (2012) BioLemmatizer: a lemmatization tool for morphological processing of biomedical text. J. Biomed. Semantics, 3, 1-29.
- https://sourceforge.net/projects/biolemmatizer/

You could indicate which preprocessing steps will be executed by assigning TRUE/FALSE for the corresponding variable within shell script:
```shell
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
```

## Execute
Execute the NLP preprocessing pipeline within the `NLP-preprocessing-pipeline` directory by using the `NLP-preprocessing-pipeline.sh` shell script. Several output files will be generated while shell script is running.
```shell
    cd NLP-preprocessing-pipeline
    ./NLP-preprocessing-pipeline.sh
```

# Automatic summarization
At present, our pipeline generates the automatic summary of only one TF at the same time (i.e. one by one). The TF name must be indicated within the shell scripts. The NLP preprocessing pipeline must be already executed, so the `features` directory must contain several files.

## Configure

### Automatic classification
You must indicate the directory path for the feature sentences (`INPUT_PATH`), the classified sentences (`OUTPUT_PATH`), and the trained classification model (`MODEL_PATH`). Also, you must indicate the name of the trained model (`MODEL`), the name of the feature employed for classification (`FEATURE`), and the name of the TF (`TF_NAME`). Do not change the names of the model and the feature.
```shell
    INPUT_PATH=../preprocessing-files/features
    OUTPUT_PATH=./classified
    MODEL_PATH=.
    MODEL=SVM_model
    FEATURE=lemma_lemma_pos_pos
    TF_NAME=MarA
```

### Making automatic summary
You must indicate the directory path to place the output automatic summary (`OUTPUT_PATH`), the directory path for the classified sentences (`INPUT_PATH`), and the name of the file with the classified sentences (`INPUT_FILE`).
```shell
    OUTPUT_PATH=../automatic-summary
    INPUT_PATH=./classified
    INPUT_FILE=$TF_NAME.txt
```

## Execution
Execute the automatic summarization pipeline within the `automatic-summarization-pipeline` directory by using the `automatic-summarization-pipeline.sh` shell script.
```shell
    cd automatic-summarization-pipeline
    ./automatic-summarization-pipeline.sh
```

## Output
A raw text file with the automatic summary of the TF is placed within `automatic-summary` directory.

## Contact
Questions can be sent to Computational Genomics Program (Center for Genomic Sciences, Mexico): cmendezc at ccg dot unam dot mx.

