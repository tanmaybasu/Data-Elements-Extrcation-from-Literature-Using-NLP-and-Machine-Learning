# Data Elements Extraction of Congestive Heart Failure from Relevant Literature
 
A systematic review identifies and collates various clinical studies and compares data
elements and results in order to provide an evidence based answer for a particular
clinical question or topic. The process is manual and involves lot of time. A tool to
automate this process is lacking. The aim of this work is to develop a framework using
natural language processing and machine learning to build information extraction
algorithms to identify data elements in a new primary publication, without having to go
through the expensive task of manual annotation to build training corpus for each data
element type. The system is developed in two stages. Initially, it uses information
contained in existing systematic reviews to identify the sentences from the PDF files of
the included references that contain specific data elements of interest using a new
similarity measure. These sentences have been treated as labeled data. A Support
Vector Machine (SVM) classifier is trained on this labeled data to extract data elements
of interests from a new article. We conducted experiments on Cochrane Database
systematic reviews related to congestive heart failure using inclusion criteria as an
example data element. The empirical results show that the proposed system
automatically identifies sentences containing the data element of interest with a high
recall (93.75\%) and reasonable precision (27.05\% - which means the reviewers have
to read only 3.7 sentences on average). The empirical results suggest that the tool is retrieving valuable information from the reference articles, even when it is time consuming to identify them manually. Thus we hope that the tool will be useful for automatic data extraction from biomedical research publications. The future scope of this work is to generalize this information framework for all types of systematic reviews. 


The analysis and performance of this framework is explained in the following paper:

[Tanmay Basu, Shraman Kumar, Abhishek Kalyan, Priyanka Jayaswal, Pawan Goyal, Stephen Pettifer, Siddhartha R Jonnalagadda. A novel framework to expedite systematic reviews by automatically building information extraction training corpora. arXiv preprint arXiv:1606.06424, 2016.](https://arxiv.org/abs/1606.06424).

## Prerequisites
[Python 3](https://www.python.org/downloads/), [Scikit-Learn](https://scikit-learn.org/0.16/install.html), [NLTK](https://www.nltk.org/install.html), [PDFX](https://pypi.org/project/pdfx/) 


## How to Run the Pipeline


* `code_included_ref_download.py`: The bibliographic information of each reference included in a systematic review are extracted from the online Cochrane Library. This code is written in Python.

* `code_getPM.java`: Titles of all included references in a systematic review are the input to these code. This java code returns a list of PubMED ids by using eutils search API. All the results which have less than 5 PubMED ids are considered to retrieve their citation information from PubMed. This is a Java code.

* `code_json_xml.java`: This code extracts inclusion statements (a data element of interest) from the JSON file corresponding to the PDF of each systematic review article. The PDF is converted to JSON using PDFx tool. The inclusion statements along with the reference are stored in XML format by this code. This code is written in Java.

* `code_extract_incl_stmt_from_xml.py`: Extracts inclusion statements from the XML files and write them into a text file along with the references where they appear. This is a python code. 

*`code_create_training_set.py`: Creates the training corpus using the inclusion statements. The code takes the text file as input, where all the inclusion statement along with the references are stored. Moreover, all the references in plain text format are taken as the input. Therefore it extracts the actual sentence for each inclusion statement from the corresponding reference and stores the output in separate files. Similarly it generates some negative sentences for each inclusion statement and store them in different files. All these output files build the gold standard. This code is written in Python.

* `code_extract_inclusion_stmt_from_test_samples.py`: The inputs to this code are the training corpus created by the earlier code and the test samples in text format. The code extracts the inclusion statements from these test samples. SVM is used as the classifier in this code. This code is written in Python. Scikit-learn, a machine learning tool is used in this code. 

## Contact

For any further query, comment or suggestion, you may reach out to me at welcometanmay@gmail.com

## Citation
```
@article{basu16dataextraction,
	title={A Novel Framework to Expedite Systematic Reviews by Automatically Building Information Extraction Training Corpora},
	author={Basu, Tanmay and Kumar, Shraman and Kalyan, Abhishek and Jayaswal, Priyanka and Goyal, Pawan and Pettifer, Stephen and Jonnalagadda, Siddhartha R},
	journal={arXiv preprint arXiv:1606.06424},
	year={2016}
}

```
