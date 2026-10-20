import urllib.request
import re
import json

url = 'https://nndepsport.nagradion.ru/tournament46746/team/448703/players'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
with urllib.request.urlopen(req) as resp:
    raw = resp.read()
    charset = resp.headers.get_content_charset() or 'utf-8'
    text = raw.decode(charset, errors='replace')

# 1. Team logo & photo
team_logo_match = re.search(r'src="(https://img\.nagradion\.ru/images/[^"]*shields/[^"]+)"', text)
team_photo_match = re.search(r'href="(https://img\.nagradion\.ru/images/big/teams/[^"]+)"', text)

team_logo = team_logo_match.group(1) if team_logo_match else ''
team_photo = team_photo_match.group(1) if team_photo_match else ''

print('Team logo:', team_logo)
print('Team photo:', team_photo)

# 2. Extract players
# Look for request_view_row_
chunks = text.split('id="request_view_row_')
players = []

for ch in chunks[1:]:
    # Player image
    img_match = re.search(r'src="(https://img\.nagradion\.ru/images/[^"]*player[^"]+)"', ch)
    img_url = img_match.group(1) if img_match else ''
    
    # Player link & name
    name_match = re.search(r'/tournament\d+/player/(\d+)[^>]*>([^<]+)</a>', ch)
    pid = name_match.group(1) if name_match else ''
    name = name_match.group(2).strip() if name_match else ''
    
    # Age & role
    # In ch, look for "лет" or number
    age_match = re.search(r'(\d+)\s*лет', ch)
    age = age_match.group(1) if age_match else ''
    
    # Role / position
    # Let's see if role is present (e.g. Вратарь, Полевой, Защитник...)
    # Look for role text
    lines = [l.strip() for l in re.sub(r'<[^>]+>', '\n', ch).split('\n') if l.strip()]
    
    # Number
    num_match = re.search(r'Игровой номер:\s*(\d+)', ch)
    number = num_match.group(1) if num_match else ''
    
    if name:
        players.append({
            'id': pid,
            'name': name,
            'number': number,
            'age': age,
            'photo': img_url,
            'raw_lines': lines[:8]
        })

print(f'Extracted {len(players)} players:')
for p in players[:5]:
    print(' ', p)

# 3. Extract coaches / officials
coach_chunks = text.split('/tournament46746/official/')
coaches = []
for c in coach_chunks[1:]:
    c_name_match = re.search(r'>([^<]+)</a>', c)
    if c_name_match:
        c_name = c_name_match.group(1).strip()
        # Find role nearby
        coaches.append(c_name)
print('Coaches:', coaches)

# 4. Extract matches
# Table class oneTourSchedule
match_rows = re.findall(r'<tr class="match_row".*?</tr>', text, re.DOTALL)
print(f'Extracted {len(match_rows)} matches:')
matches = []
for mr in match_rows:
    tour_match = re.search(r'class="move_handle">(\d+)</td>', mr)
    tour = tour_match.group(1) if tour_match else ''
    
    date_match = re.search(r'data-sort-value="(\d+)"[^>]*>\s*([^<]+)\s*</td>', mr)
    date_str = date_match.group(2).strip() if date_match else ''
    
    teams = re.findall(r'/tournament\d+/team/\d+/players"[^>]*>\s*([^<]+)\s*</a>', mr)
    
    venue_match = re.search(r'ФОК [^<]+', mr)
    venue = venue_match.group(0) if venue_match else 'ФОК "Приокский"'
    
    # Result or link
    mid_match = re.search(r'data-match-id="(\d+)"', mr)
    mid = mid_match.group(1) if mid_match else ''
    
    score_match = re.search(r'>(\d+\s*:\s*\d+)<', mr)
    score = score_match.group(1) if score_match else '— : —'
    
    matches.append({
        'tour': tour,
        'date': date_str,
        'team1': teams[0].strip() if len(teams) > 0 else '',
        'team2': teams[1].strip() if len(teams) > 1 else '',
        'venue': venue,
        'match_id': mid,
        'score': score
    })

for m in matches:
    print(' ', m)

with open('extracted_data.json', 'w', encoding='utf-8') as f:
    json.dump({
        'team_name': 'Доза Агро',
        'city': 'Нижний Новгород',
        'tournament': 'Первая лига-2026/2027',
        'team_logo': team_logo,
        'team_photo': team_photo,
        'players': players,
        'coaches': coaches,
        'matches': matches
    }, f, ensure_ascii=False, indent=2)

print('Saved extracted_data.json successfully!')
