import json 

data = json.load(open('genomicVariations.json_genesinallchrs'))

chr_value = 'chr19'

filtered_data = [item for item in data if item.get('variation', {}).get('location', {}).get('chr') == chr_value]

with open('genomicVariations.json', "w") as f:
    json.dump(filtered_data, f, indent=4)