######################################################################
#  CliNER - train.py                                                 #
#                                                                    #
#  Willie Boag                                      wboag@cs.uml.edu #
#                                                                    #
#  Purpose: Build model for given training data.                     #
######################################################################


import os
import os.path
import glob
import argparse
import pickle
import sys

import tools
from model import ClinerModel
from notes.documents import Document

# base directory
CLINER_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    filepath = "F:/Programming Documnets/AI/Telehealth/CliNER-master/data/examples/ex_doc.txt"
    train_txt_files = glob.glob(filepath)

    filecon = "F:/Programming Documnets/AI/Telehealth/CliNER-master/data/examples/ex_doc.con"
    train_con_files = glob.glob(filecon)

    # Collect training data file paths
    train_txt_files_map = tools.map_files(train_txt_files) 
    train_con_files_map = tools.map_files(train_con_files)

    training_list = []
    for k in train_txt_files_map:
        if k in train_con_files_map:
            training_list.append((train_txt_files_map[k], train_con_files_map[k]))

    # Train the model

    default_log = os.path.join(CLINER_DIR, 'models', 'train.log')
    default_use_lstm = False
    val_list = []
    test_list = []

    filemodel = "F:/Programming Documnets/AI/Telehealth/CliNER-master/models/foo.model"
    model = os.fspath(filemodel)

    train(training_list, model, 'i2b2', default_use_lstm, default_log, val = val_list, test = test_list)



def train(training_list, model_path, format, use_lstm, logfile=None, val=[], test=[]):

    # Read the data into a Document object
    train_docs = []
    for txt, con in training_list:
        doc_tmp = Document(txt,con)
        train_docs.append(doc_tmp)

    val_docs = []
    for txt, con in val:
        doc_tmp = Document(txt,con)
        val_docs.append(doc_tmp)

    test_docs = []
    for txt, con in test:
        doc_tmp = Document(txt,con)
        test_docs.append(doc_tmp)

    # file names
    if not train_docs:
        print( 'Error: Cannot train on 0 files. Terminating train.')
        return 1

    # Create a Machine Learning model
    model = ClinerModel(use_lstm)

    # Train the model using the Documents's data
    model.train(train_docs, val=val_docs, test=test_docs)

    # Pickle dump
    print('\nserializing model to %s\n' % model_path)
    with open(model_path, "wb") as m_file:
        pickle.dump(model, m_file)
        
    model.log(logfile   , model_file=model_path)
    model.log(sys.stdout, model_file=model_path)
    


if __name__ == '__main__':
    main()
