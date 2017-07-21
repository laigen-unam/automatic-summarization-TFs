# Automatic summarization of transcription factor properties

In the BioNLP group of the Computational Genomics Program, we conduct research on automatic text summarization for helping the biocuration process of RegulonDB (http://regulondb.ccg.unam.mx/).

RegulonDB is a database dedicated to the transcriptional regulation of Escherichia coli K-12. This database contains a set of summaries about several properties of TFs. These summaries are also found in EcoCyc (https://ecocyc.org/). These summaries are written manualy by using several scientific articles.

We have proposed an initial approach for the automaticaly generation of these summaries. In this initial approach we generate summaries only about two properties of TFs:
1.	The biological processes in which the regulated genes are involved
2.	The number, name, and size of the structural domains constituting the TF

The automatic summaries are made by the concatenation of the automatically classified sentences from scientific articles by an SVM classifier. The evaluation of these initial automatic summaries indicated that they carried part of the relevant information included in the manual summaries.
 
This repository provides a pipeline for generating these initial automatic summaries.

Questions can be sent to Computational Genomics Program, Center for Genomic Sciences, cmendezc at ccg.unam.mx.


