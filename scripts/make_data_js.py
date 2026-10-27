import json

with open('site_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

js_content = f"// Nagradion Redesign - Clean Data Export\nwindow.SITE_DATA = {json.dumps(data, ensure_ascii=False, indent=2)};\n"

with open('data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print('Generated data.js successfully!')
