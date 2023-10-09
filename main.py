
import csv
import sys
from github import Github
from bs4 import BeautifulSoup
from knowledge_graph import construct_kg
from relation_extractor import Stanford_Relation_Extractor
from create_structured_csv import create_csv
from csv_utils import convert_to_json, clean_commits_csv, clean_readme_csv
import os

# using an access token
g = Github("")


def kg_commits(repo,file_name):
    print("Constructing commits KG")
    commits = repo.get_commits(path=file_name)

    commits_list = []

    for commit in commits:
        commits_list.append(commit)
    print("Number of commits:",len(commits_list))
    commits_list.reverse()
    index = 0
    while index<len(commits_list):
        commit = commits_list[index]       
        index=index+1
        print("Processing Commit: ",index)    
        additions = ""
        deletions = ""

        for _file in commit.files:
            if _file.filename != file_name:
                continue
            patch = _file.patch
            
            if patch is None:
                patch=""
            patch_lines = patch.split("\n")
            
                # f.seek(0)
                # f.truncate()
            for line in patch_lines:
                if len(line) == 0 or len(line)==1:
                    continue
                if line[0] == "+" :
                    additions += (line[1:]+"\n")              
                    
                elif line[0]== "-":
                    deletions += (line[1:]+"\n")              
                    
            
        
        with open('./data/input/input_data.txt','w+') as f:
            f.write(additions)
        f.close()
        if len(additions) == 0:
            continue

     
        construct_kg(additions)
        Stanford_Relation_Extractor()
        create_csv(commit.commit.committer.date, commit.sha, "", "addition")

        if len(deletions) == 0:
            continue
      

        with open('./data/input/input_data.txt','w+') as f:
            f.write(deletions)
        f.close()
        construct_kg(deletions)
        Stanford_Relation_Extractor()
        create_csv(commit.commit.committer.date, commit.sha, "", "deletion")
    print("Commits KG completed")
                  

def kg_readme(repo,file_name):
    print("Constructing KG on readme...")
    readme = repo.get_contents(file_name)
    text = readme.decoded_content
    cleantext = BeautifulSoup(text, "lxml").text

    with open('./data/input/input_data.txt','w+') as f:
            f.write(cleantext)
    f.close()
    construct_kg(cleantext)
    Stanford_Relation_Extractor()
    create_csv("", "", "readme", "")
    print("Completed construction of KG on readme.")
   




if __name__ == "__main__":

    


    repo = g.get_repo(sys.argv[1])
    
  
    print(repo.full_name)
    file_name = ""
    contents = repo.get_contents("")
    while len(contents)>0:
        file_content = contents.pop(0)
        if file_content.name.lower() == "readme.md":
            file_name = file_content.name
            break
    print(file_name)
    
    
    clean_commits_csv('./data/result/named_entity_input_data_.csv','./results/commits_'+repo.name+'.csv')
    kg_commits(repo,file_name)
    convert_to_json('./results/commits_'+repo.name+'.csv','./results/commits_'+repo.name+'.json')
    kg_readme(repo,file_name)
    clean_readme_csv('./data/result/named_entity_input_data_readme.csv','./results/readme_'+repo.name+'.csv')

    with open('./data/result/named_entity_input_data_.csv','w') as out:
        writer = csv.DictWriter(out, fieldnames=['Type','Entity 1','Relationship','Type','Entity2','Date','Sha','Change'])
        writer.writeheader()
    with open('./data/result/named_entity_input_data_readme.csv','w') as out:
        writer = csv.DictWriter(out, fieldnames=['Type','Entity 1','Relationship','Type','Entity2','Date','Sha','Change'])
        writer.writeheader()
    
    
    



