# TREC-2017-PM-CDS-Track

## Synopsis
The Text REtrieval Conference (TREC), co-sponsored by the National Institute of Standards and Technology (NIST) and U.S. Department of Defense, is a series of workshops that focus on Information Retrieval research. <br>
It has different research areas (called tracks) and each track has different challenges in which particular retrieval tasks are defined. <br>
The aim for TREC 2017 Precision Medicine Track was to provide useful information to physicians for treating cancer patients. <br>
This is a small part of my codebase that I used for the TREC 2017 Precision Medicine/Clinical Decision Support Track. <br>

## Usage
It mainly contains two programs (and they should be run in the following order): <br>
1. extract_xml_to_elastic.py
* It reads the data from the input xml files and indexes it in Elasticsearch.
* The input dataset this is currently configured to work on is the clinical trials dataset (which has over 2,41,006 xml files).
* You will need to modify the path to the input xml files on line 27.
2. query_elasticsearch.py
* It queries Elasticsearch with different query topics and writes the output to a file.
* The output is a text file with retrieved results for each query in the standard trec_eval format.
* You will need to modify the path to the query xml file on line 25.
* You might want to change the name and location of the output text files on line 102 as per your preference.
<br>

After making the necessary modifications, the above programs can simply be executed from the command line as shown below.
```sh
python extract_xml_to_elastic.py
```
and
```sh
python query_elasticsearch.py
```
The Elasticsearch version used for this project is 5.5.0 and Python version used is 2.7.12.



## Useful Links
[TREC](http://trec.nist.gov/) <br>
[TREC 2017 Precision Medicine/Clinical Decision Support Track](http://trec-cds.appspot.com/2017.html) <br>
[Elasticsearch](https://www.elastic.co/products/elasticsearch) <br>
[Elasticsearch Python API](https://elasticsearch-py.readthedocs.io/en/master/) <br>
