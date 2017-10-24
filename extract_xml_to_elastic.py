#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 13:53:40 2017

@author: aj

This program extracts the desired data from the input xml files and indexes it in Elasticsearch.
The input files this program currently works on is the clinical trials dataset provided in the TREC 2017 Precision Medicine/ Clinical Decision Support Track. More information about this can be found here: http://trec-cds.appspot.com/2017.html
"""


import glob
import xml.etree.ElementTree as ET
import collections
import elasticsearch_copy
import time


def extract_data_xml():
       """
       This function is used to extract the desired data from the input xml files.
       After extracting the desired data from each input xml file, it is stored in an ordered dictionary. This dictionary is then passed to the elastic_index function which will index the data in Elasticsearch.
       """
       
       #Provide the path to the input xml files
       list_of_files = glob.glob('/home/aj/Downloads/TREC/input/clinicaltrials_xml/*/*' + '/*.xml')
       
       #Counter variable to count each processed file
       ctr = 0
       
       #We will print the progress as we process each file
       print '\nProgress:'
       
       #This for loop iterates over each input file. Within each try-except block we try to extract the data from one particular xml field. This extracted data is stored in an ordered dictionary with key as the field name and value as the extracted data.
       #Currently the following fields are extracted: nct_id, brief_title, brief_summary, detailed_description, overall_status, condition, eligibility, gender, gender_based, minimum_age, maximum_age, keyword, mesh_term
       #Not all the files contain all the fields we desire, hence the multiple try-except blocks.
       for input_file in list_of_files:
              tree = ET.parse(input_file)
              root = tree.getroot()
              
              #Create an ordered dictionary and lists to store the keywords and mesh terms
              extracted_data = collections.OrderedDict()
              keyword_list = []
              mesh_term_list = []
              
              #nct_id
              try:
                     nct_id = root.find('id_info').find('nct_id').text
                     extracted_data['nct_id'] = nct_id
              except:
                     extracted_data['nct_id'] = None

              #brief_title
              try:
                     brief_title = root.find('brief_title').text
                     extracted_data['brief_title'] = brief_title
              except:
                     extracted_data['brief_title'] = None

              #brief_summary
              try:
                     brief_summary = root.find('brief_summary').find('textblock').text
                     extracted_data['brief_summary'] = brief_summary
              except:
                     extracted_data['brief_summary'] = None

              #detailed_description
              try:
                     detailed_description = root.find('detailed_description').find('textblock').text
                     extracted_data['detailed_description'] = detailed_description
              except:
                     extracted_data['detailed_description'] = None

              #overall_status
              try:
                     overall_status = root.find('overall_status').text
                     extracted_data['overall_status'] = overall_status
              except:
                     extracted_data['overall_status'] = None

              #condition
              try:
                     condition = root.find('condition').text
                     extracted_data['condition'] = condition
              except:
                     extracted_data['condition'] = None

              #eligibility
              try:
                     eligibility = root.find('eligibility').find('criteria').find('textblock').text
                     extracted_data['eligibility'] = eligibility
              except:
                     extracted_data['eligibility'] = None

              #gender
              try:
                     gender = root.find('eligibility').find('gender').text
                     extracted_data['gender'] = gender
              except:
                     extracted_data['gender'] = None

              #gender_based
              try:
                     gender_based = root.find('eligibility').find('gender_based').text
                     extracted_data['gender_based'] = gender_based
              except:
                     extracted_data['gender_based'] = None

              #minimum_age
              try:
                     minimum_age = root.find('eligibility').find('minimum_age').text
                     try:
                            extracted_data['minimum_age'] = int(minimum_age.split(' ')[0])
                     except:
                            extracted_data['minimum_age'] = 0
              except:
                     extracted_data['minimum_age'] = None

              #maximum_age
              try:
                     maximum_age = root.find('eligibility').find('maximum_age').text
                     try:
                            extracted_data['maximum_age'] = int(maximum_age.split(' ')[0])
                     except:
                            extracted_data['maximum_age'] = 99
              except:
                     extracted_data['maximum_age'] = None

              #keyword
              try:
                     keyword = root.findall('keyword')
                     for index, item in enumerate(keyword):
                            keyword_list.append(item.text)
                     extracted_data['keyword'] = keyword_list
              except:
                     extracted_data['keyword'] = None

              #mesh_term
              try:
                     mesh_term = root.find('condition_browse').findall('mesh_term')
                     for index, item in enumerate(mesh_term):
                            mesh_term_list.append(item.text)
                     extracted_data['mesh_term'] = mesh_term_list
              except:
                     extracted_data['mesh_term'] = None
              
              #Pass the counter 'ctr' and the dictionary 'extracted_data' to elastic_index function which indexes it in Elasticsearch.
#              elastic_index(ctr, extracted_data)
              
              #Increment the counter and print the progress in the following format: current counter value/total number of input files.
              ctr+=1
              print ctr,'/',len(list_of_files)


#Insert elastic_index function here to index data in Elasticsearch




#Note the start time
start_time = time.time()


if __name__ == '__main__':
       #Create connection to Elasticsearch listening on localhost port 9200. It uses the Python Elasticsearch API which is the official low-level client for Elasticsearch.
       es = elasticsearch_copy.Elasticsearch([{'host': 'localhost', 'port': 9200}])
       #Call the function to start extracting the data
       extract_data_xml()


#Print the total execution time
print("\nExecution time: %.2f seconds" %(time.time()-start_time))