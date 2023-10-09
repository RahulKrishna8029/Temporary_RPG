import pickle
import pandas as pd
import os
import csv
import glob

def is_non_zero_file(fpath):  
    if os.path.isfile(fpath) and os.path.getsize(fpath) <= 0:
        return False
    file = open(fpath)
    csvreader = csv.reader(fpath)
    
    return True

def create_csv(commit_date,commit_sha, type, change):
    
     #create a list of pickle file names
    pickles = []
    for file in glob.glob(os.getcwd() + "/data/output/ner/*.pickle"):
        pickles.append(file)

    #load each pickle file and create the resultant csv file
    for file in pickles:
        with open(file,'rb') as f:
            entities = pickle.load(f)

        #add all the names in entity set
        entity_set = set(entities.keys())
        final_list = []
        curr_dir = os.getcwd()
        file_name_list = file.split('/')[-1].split('.')[0].split('_')[2:]
        file_name = file_name_list[0]
        flag = True
        for str in file_name_list[1:]:
            file_name += '_'
            file_name += str
            

        file_path = curr_dir +"/data/output/kg/"+file_name+".txt-out.csv"
        
        if is_non_zero_file(file_path) is False:
            return
        df = None
        try:
            df = pd.read_csv(file_path)
        except pd.errors.EmptyDataError:
            df = pd.DataFrame()     
        
        
        #parse every row present in the intermediate csv file
        triplet = set()
        for i,j in df.iterrows():
            j[0] = j[0].strip()
            #if entity is present in entity set, only then parse futrther
            if j[0] in entity_set:
                added = False
                e2_sentence = j[2].split(' ')
                #check every word in entity2, and add a new row triplet if it is present in entity2
                for entity in e2_sentence:
                    if entity in entity_set:
                        _ = (entities[j[0]], j[0], j[1] ,entities[entity], j[2], commit_date, commit_sha, change )
                        triplet.add(_)
                        added = True
                if not added:
                    _ = (entities[j[0]], j[0], j[1] ,'O', j[2],commit_date, commit_sha, change)
                    triplet.add(_)
        #convert the pandas dataframe into csv
        
        if len(triplet) != 0:
            path = './data/result/' + file.split("/")[-1].split(".")[0] + "_"+type + '.csv'
           
            processed_pd = pd.DataFrame(list(triplet))
            
            processed_pd.to_csv(path, encoding='utf-8', index=False, mode='a')

   