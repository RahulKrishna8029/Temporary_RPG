import os
import subprocess
import glob
import pandas as pd

def Stanford_Relation_Extractor():

    
    

    for f in glob.glob(os.getcwd() + "/data/output/kg/*.txt"):        
        
        current_directory = os.getcwd()
        
        os.chdir(current_directory + '/stanford-openie')
        
        path = './process_large_corpus.sh'
   
        p = subprocess.Popen(['sh', './process_large_corpus.sh', f, f + '-out.csv'], stdout=subprocess.PIPE)

        output, err = p.communicate()
        os.chdir(current_directory)
        
   

    
    


if __name__ == '__main__':
    Stanford_Relation_Extractor()
