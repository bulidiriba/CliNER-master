######################################################################
#  CliNER - predict.py                                               #
#                                                                    #
#  Willie Boag                                      wboag@cs.uml.edu #
#                                                                    #
#  Purpose: Use trained model to predict concept labels for data.    #
######################################################################


import os
import sys
import glob
import argparse
import itertools
import pickle

import tools
from model import ClinerModel, write
from notes.documents import Document
import copy

def main():

    txt = []
    line = input('write text:-\n')
    while line:
        txt.append(line)
        line = input()

    filepath = "F:/Programming Documnets/AI/Telehealth/CliNER-master/data/test_predictions/ex_doc.txt"
    file = open(filepath, 'w')
    for i in txt:
        file.write(i + "\n")
    file.close()

    #filepath = "F:/Programming Documnets/AI/Telehealth/CliNER-master/data/examples/ex_doc.txt"

    files = glob.glob(filepath)

    outputpath = "F:/Programming Documnets/AI/Telehealth/CliNER-master/data/test_predictions/"
    tools.mkpath(outputpath)

    filemodel = "F:/Programming Documnets/AI/Telehealth/CliNER-master/models/foo.model"
    model = os.fspath(filemodel)

    # Predict
    predict(files, model, outputpath, format='i2b2')


def predict(files, model_path, output_dir, format, use_lstm=True):

    # Must specify output format
    if format not in ['i2b2']:
        sys.stderr.write('\n\tError: Must specify output format\n')
        sys.stderr.write('\tAvailable formats: i2b2\n')
        sys.stderr.write('\n')
        exit(1)

    # Load model
    #if use_lstm==False:
    with open(model_path, 'rb') as f:
        model = pickle.load(f,encoding = 'latin1')
       
        
    if model._use_lstm:
        import helper_dataset as hd
        import DatasetCliner_experimental as Exp
        import entity_lstm as entity_model
        
        parameters=hd.load_parameters_from_file("LSTM_parameters.txt")  
        parameters['use_pretrained_model']=True

        temp_pretrained_dataset_adress=parameters['model_folder']+os.sep+"dataset.pickle"
        model._pretrained_dataset = pickle.load(open(temp_pretrained_dataset_adress, 'rb'))
        model._pretrained_wordvector=hd.load_pretrained_token_embeddings(parameters)
        model._current_model=None

        print ("END TEST")
        #exit()
        #model.parameters=None

    # Tell user if not predicting
    if not files:
        sys.stderr.write("\n\tNote: You did not supply any input files\n\n")
        exit()
    
    n = len(files)

    
    for i,txt in enumerate(sorted(files)):
        note = Document(txt)
        # Output file
        fname = os.path.splitext(os.path.basename(txt))[0] + '.' + 'con'
        out_path = os.path.join(output_dir, fname)


        
        if os.path.exists(out_path):
            print()
            #print('\tWARNING: prediction file already exists (%s)' % out_path)
            #continue
        

        '''
        sys.stdout.write('%s\n' % ('-' * 30))
        sys.stdout.write('\n\t%d of %d\n' % (i+1,n))
        sys.stdout.write('\t%s\n\n' % txt)
        '''
        # Predict concept labels
        labels = model.predict_classes_from_document(note)

        # Get predictions in proper format
        output = note.write(labels)

        print("-----------OUTPUT----------\n")
        print(output)

        # Output the concept predictions
        sys.stdout.write('\n\nwriting to: %s\n' % out_path)
        with open(out_path, 'w') as f:
            write(f, '%s\n' % output)
        sys.stdout.write('\n')



if __name__ == '__main__':
    main()
