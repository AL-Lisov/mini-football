import re

with open('raw_bytes.bin', 'rb') as f:
    text = f.read().decode('utf-8', errors='replace')

chunks = text.split('id="request_view_row_')
for ch in chunks[1:]:
    name_m = re.search(r'/tournament\d+/player/\d+[^>]*>\s*([^<]+)\s*</a>\s*</strong>\s*<br/>\s*([^<]+)<br/>', ch)
    # Search for number anywhere in chunk
    num_m = re.search(r'Игровой номер:\s*</span>\s*(\d+)', ch)
    if not num_m:
        num_m = re.search(r'Игровой номер:[^<]*<[^>]*>(\d+)', ch)
    if not num_m:
        num_m = re.search(r'Игровой номер:\s*(\d+)', ch)
    
    # check role
    role = 'Полевой'
    if 'Вратарь' in ch or 'вратарь' in ch.lower():
        role = 'Вратарь'
    elif 'Защитник' in ch or 'защитник' in ch.lower():
        role = 'Защитник'
    elif 'Нападающий' in ch or 'нападающий' in ch.lower():
        role = 'Нападающий'

    # Age
    age_m = re.search(r'(\d+)\s*лет', ch)
    
    if name_m:
        name = f'{name_m.group(1).strip()} {name_m.group(2).strip()}'
        num = num_m.group(1) if num_m else ''
        age = age_m.group(1) if age_m else ''
        # print to file or check
        print(f"{name:25} | №: {num:4} | {age:3} лет | {role}")
