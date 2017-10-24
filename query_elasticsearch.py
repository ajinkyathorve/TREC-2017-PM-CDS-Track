#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 17:24:22 2017

@author: aj

This program queries Elasticsearch with each individual query and writes the retrieved results to an output file in the standard trec_eval format.
There are 30 query topics provided for which this program retrieves the search results. More information about this can be found here: http://trec-cds.appspot.com/2017.html
"""


import xml.etree.ElementTree as ET
import collections
import elasticsearch_copy


def extract_query_xml():
       """
       The query topics are provided in an XML file. This function is used to extract query terms from that XML file.
       After extracting the query terms, it is stored in an ordered dictionary. This dictionary is then passed to the es_query function which will query Elasticsearch with those terms.
       """
       
       #Provide the path to the query xml file
       query_file = file('/home/aj/Downloads/TREC/input/topics/topics2017.xml')
       
       tree = ET.parse(query_file)
       root = tree.getroot()
       
       #Create an ordered dictionary to store the query terms
       extracted_data = collections.OrderedDict()
       
       #There are 30 query topics provided. First we store all the topics and iterate over each of them using a for loop.
       #Each query topic contains multiple fields. In the try-except block we try to extract the terms for each particular query. These extracted terms are stored in an ordered dictionary with key as the field name and value as the extracted terms.
       try:
              topics = root.findall('topic')
              for index, item in enumerate(topics):
                     tnum = index+1
                     disease = item.find('disease').text
                     gene = item.find('gene').text
                     demographic = item.find('demographic').text
                     other = item.find('other').text
                     extracted_data['tnum'] = tnum
                     extracted_data['disease'] = disease
                     extracted_data['gene'] = gene
                     extracted_data['age'] = int(demographic.split('-')[0])
                     extracted_data['sex'] = demographic.split(' ')[1]
                     extracted_data['other'] = other
                     es_query(extracted_data)
       except:
              extracted_data['tnum'] = None
              extracted_data['disease'] = None
              extracted_data['gene'] = None
              extracted_data['age'] = None
              extracted_data['sex'] = None
              extracted_data['other'] = None

       return


def es_query(extracted_data):
       """
       This function is used to query Elasticsearch and write results to an output file.
       It receives a dictionary containing the extracted query terms from the extract_query_xml function. After querying Elasticsearch, the retrieved results are written to an output file in the standard trec_eval format.
       """
       
       try:
              #Store the disease name from the received dictionary in the variable named query
              query = extracted_data['disease']
              #For a simple query without any customizations, uncomment the following line
              #res = es.search(index='ct', q=query, size=1000)['hits']['hits']
              #Current implementation uses a customized query with multi-match and post-filters in a manner deemed best possible for the current retrieval process. Comment the following query if you plan to use the simple query in the previous line.
              #We limit the retrieved results to 1000. The results are arranged in decreasing order of their assigned scores. We assign a rank to each result starting from 1 to 1000 based on decreasing scores. We normalize the score for each result based on the score of the first result with the maximum score.
              res = es.search(index='ct', body={
                                          "query":
                                                 {"bool":
                                                        {"must":
                                                               {"multi_match":
                                                                      {"query":query, "type":"phrase_prefix", "fields":["brief_title","brief_summary","detailed_description","condition", "eligibility","keyword","mesh_term"]
                                                                      }
                                                               },
                                                         "should":
                                                                [
                                                                 {"term":{"eligibility" : "query"}},
                                                                 {"term":{"brief_summary" : "query"}},
                                                                 {"term":{"detailed_description" : "query"}},
                                                                 {"term":{"keyword" : "query"}},
                                                                ]
                                                        }
                                                 },
                                          "post_filter":
                                                 {"term":
                                                        {"gender":"all"}
                                                 }
                                          },
                                   size=1000
                     )['hits']['hits']
              max_score = res[0]['_score']
              rank_ctr = 1
              
              #Write the retrieved results to an output file in the standard trec_eval format
              with open('/home/aj/Downloads/TREC/output/ub_trec_pm_2017_ct_run100.txt', 'a') as op_file:
                     for i in res:
                            op_file.write('{}\tQ0\t{}\t{}\t{}\t2_ec_complex\n'.format(extracted_data['tnum'],i['_source']['nct_id'],rank_ctr,round(i['_score']/max_score,4)))
                            rank_ctr += 1
               
       except Exception as e:
              print "\nUnable to query/write!"
              print 'Error Message:',e,'\n'
       
       return




if __name__ == '__main__':
       #Create connection to Elasticsearch listening on localhost port 9200. It uses the Python Elasticsearch API which is the official low-level client for Elasticsearch.
       try:
              es = elasticsearch_copy.Elasticsearch([{'host': 'localhost', 'port': 9200}])
       except Exception as e:
              print '\nCannot connect to Elasticsearch!'
              print 'Error Message:',e,'\n'
       #Call the function to start extracting the queries
       extract_query_xml()