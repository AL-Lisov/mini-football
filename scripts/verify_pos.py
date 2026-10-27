import json

with open('site_data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

for p in d['players']:
    if any(k in p['name'] for k in ['Лисов', 'Орехов', 'Кожин', 'Яблочков']):
        print(f"{p['name']} -> {p['position']}")
