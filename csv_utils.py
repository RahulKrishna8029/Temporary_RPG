import csv
import json

def convert_to_json(path, out_path):
    data = {
        "commits":{}
    }
    
    with open(path) as f:
        csv_reader = csv.DictReader(f)

        for rows in csv_reader:
            
            if rows['Change'] != 'addition' and rows['Change'] != 'deletion':
                continue
            key = rows['Sha']
            #print(rows)
            if key not in data['commits']:
                # commit id is not present
                commit_data = {}
                commit_data['date'] = rows['Date']
                commit_data['additions']=[]
                commit_data['deletions']=[]
                data['commits'][key]=commit_data


            
            data['commits'][key][rows['Change']+'s'].append(rows)
    
    with open(out_path, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))

def clean_commits_csv(input_path, output_path):
    with open(input_path,'r') as inp, open(output_path,'w') as out:
        field_names = ['Entity 1','Relationship','Entity2','Date','Sha','Change']
        csv_reader = csv.DictReader(inp)
        writer = csv.DictWriter(out,fieldnames=field_names)
        writer.writeheader()
        for rows in csv_reader:
            if rows['Change'] != 'addition' and rows['Change'] != 'deletion':
                continue
            csv_row = rows.copy()
            del csv_row["Type"]
            writer.writerow(csv_row)

def clean_readme_csv(input_path, output_path):
    with open(input_path,'r') as inp, open(output_path,'w') as out:
        field_names = ['Entity 1','Relationship','Entity2']
        csv_reader = csv.DictReader(inp)
        writer = csv.DictWriter(out,fieldnames=field_names)
        writer.writeheader()
        for rows in csv_reader:
            triplet = rows.copy()
            del triplet["Type"], triplet["Change"], triplet["Date"], triplet["Sha"]            
            writer.writerow(triplet)


if __name__ == "__main__":
    convert_to_json('input.csv')

# Type,Entity 1,Relationship,Type,Entity2,Date,Sha
# {
#   "commits": {
#     "commit_id": {
#       "date": "",
#       "additions": [],
#       "deletions": []
#     }
#   }
# }
