import csv
import json

def write_and_process_changes(changes, change_type, pull_request_details):
    if len(changes) == 0:
        return

    # Assuming construct_kg, Stanford_Relation_Extractor, and create_csv functions exist
    construct_kg(changes)
    Stanford_Relation_Extractor()
    create_csv(pull_request_details['date_closed'], pull_request_details['number'], pull_request_details['author'], change_type)

    # Additional step: create cleaned CSV
    create_cleaned_csv('commits.csv', 'cleaned_commits.csv')

def create_cleaned_csv(input_path, output_path):
    with open(input_path, 'r') as inp, open(output_path, 'w') as out:
        field_names = ['Entity 1', 'Relationship', 'Entity2', 'Date', 'Sha', 'Change']
        csv_reader = csv.DictReader(inp)
        writer = csv.DictWriter(out, fieldnames=field_names)
        writer.writeheader()
        for rows in csv_reader:
            if rows['Change'] in ('addition', 'deletion'):
                csv_row = {key: value for key, value in rows.items() if key not in ['Type']}
                writer.writerow(csv_row)

def convert_csv_to_json(input_path, output_path):
    data = {
        "commits": {}
    }

    with open(input_path) as f:
        csv_reader = csv.DictReader(f)

        for rows in csv_reader:
            if rows['Change'] not in ('addition', 'deletion'):
                continue

            key = rows['Sha']

            if key not in data['commits']:
                commit_data = {
                    'date': rows['Date'],
                    'additions': [],
                    'deletions': []
                }
                data['commits'][key] = commit_data

            data['commits'][key][rows['Change'] + 's'].append(rows)

    with open(output_path, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))
"""

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

"""
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
