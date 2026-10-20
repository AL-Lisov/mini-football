import json
import re

with open('raw_bytes.bin', 'rb') as f:
    text = f.read().decode('utf-8', errors='replace')

team_logo_match = re.search(r'src="(https://img\.nagradion\.ru/images/[^"]*shields/[^"]+)"', text)
team_photo_match = re.search(r'href="(https://img\.nagradion\.ru/images/big/teams/[^"]+)"', text)

team_logo = team_logo_match.group(1) if team_logo_match else ''
team_photo = team_photo_match.group(1) if team_photo_match else ''

# Extract players
chunks = text.split('id="request_view_row_')
players = []

for ch in chunks[1:]:
    # Player image
    img_match = re.search(r'src="(https://img\.nagradion\.ru/images/[^"]*player[^"]+)"', ch)
    img_url = img_match.group(1) if img_match else ''
    
    # Player id, surname, first_name
    surname_match = re.search(r'/tournament\d+/player/(\d+)[^>]*>\s*([^<]+)\s*</a>\s*</strong>\s*<br/>\s*([^<]+)<br/>', ch)
    pid = surname_match.group(1) if surname_match else ''
    surname = surname_match.group(2).strip() if surname_match else ''
    first_name = surname_match.group(3).strip() if surname_match else ''
    
    # Age
    age_match = re.search(r'(\d+)\s*лет', ch)
    age = age_match.group(1) if age_match else ''
    
    # Number - note: "Номер игрока:\s*(\d+)"
    num_match = re.search(r'Номер игрока:\s*(\d+)', ch)
    number = num_match.group(1) if num_match else ''
    
    # Mini-football positions:
    # Лисов Александр и Орехов Александр — вратари. Остальные — полевые / универсалы / защитники / нападающие
    pos = 'Полевой'
    if pid in ['1242087', '1333857']: # Лисов Александр, Орехов Александр
        pos = 'Вратарь'
    elif pid in ['1190379']: # Балашов (тренер/капитан)
        pos = 'Универсал'
    elif pid in ['1333853']: # Баринов
        pos = 'Защитник'
    elif pid in ['1223265']: # Рябков
        pos = 'Защитник'
    elif pid in ['1333855']: # Драгов
        pos = 'Нападающий'
    elif pid in ['1333856']: # Кельгин
        pos = 'Нападающий'
    elif pid in ['1198226']: # Кожин
        pos = 'Полевой'
    elif pid in ['1333863']: # Яблочков
        pos = 'Полевой'
    
    if surname:
        players.append({
            'id': pid,
            'name': f'{surname} {first_name}'.strip(),
            'surname': surname,
            'first_name': first_name,
            'number': number if number else '—',
            'age': age,
            'position': pos,
            'photo': img_url,
            'matches_played': 0,
            'goals': 0,
            'assists': 0,
            'yellow_cards': 0,
            'red_cards': 0
        })

# Coaches
coaches = [
    {
        'name': 'Павлюк Александр',
        'role': 'Руководитель команды',
        'photo': 'https://img.nagradion.ru/images/small/m/playerac2d91dcabaf0009494f10c994c5ffff.jpg'
    },
    {
        'name': 'Балашов Максим',
        'role': 'Тренер / Капитан',
        'photo': 'https://img.nagradion.ru/images/small/m/player0ed34af96bbb2dcc08bc7340b192dc53.jpg'
    }
]

# Matches
match_rows = re.findall(r'<tr class="match_row".*?</tr>', text, re.DOTALL)
matches = []
for mr in match_rows:
    tour_match = re.search(r'class="move_handle">(\d+)</td>', mr)
    tour = tour_match.group(1) if tour_match else ''
    
    date_match = re.search(r'data-sort-value="(\d+)"[^>]*>\s*([^<]+)\s*</td>', mr)
    date_raw = date_match.group(2).strip() if date_match else ''
    date_clean = re.sub(r'\s+', ' ', date_raw)
    
    teams = re.findall(r'/tournament\d+/team/\d+/players"[^>]*>\s*([^<]+)\s*</a>', mr)
    team1 = re.sub(r'\s+', ' ', teams[0]).strip() if len(teams) > 0 else 'Продтерминал'
    team2 = re.sub(r'\s+', ' ', teams[1]).strip() if len(teams) > 1 else 'Доза Агро'
    
    mid_match = re.search(r'data-match-id="(\d+)"', mr)
    mid = mid_match.group(1) if mid_match else ''
    
    venue = 'ФОК "Приокский"'
    
    # Specific date cleaning
    if '19.10.2026' in date_clean:
        date_display = '19 окт 2026, 21:10'
        status = 'next'
        score = '— : —'
    else:
        date_display = 'Дата уточняется'
        status = 'scheduled'
        score = '— : —'
    
    matches.append({
        'tour': tour,
        'date': date_display,
        'team1': team1,
        'team2': team2,
        'venue': venue,
        'match_id': mid,
        'score': score,
        'status': status
    })

# Also add tournament standings summary for Primeira Liga 2026/2027
standings = [
    {'pos': 1, 'team': 'Доза Агро', 'city': 'Н.Новгород', 'games': 1, 'w': 1, 'd': 0, 'l': 0, 'goals': '4-1', 'diff': '+3', 'points': 3, 'form': ['W']},
    {'pos': 2, 'team': 'Промавто', 'city': 'Н.Новгород', 'games': 1, 'w': 1, 'd': 0, 'l': 0, 'goals': '3-1', 'diff': '+2', 'points': 3, 'form': ['W']},
    {'pos': 3, 'team': 'МясиКо', 'city': 'Н.Новгород', 'games': 1, 'w': 1, 'd': 0, 'l': 0, 'goals': '5-3', 'diff': '+2', 'points': 3, 'form': ['W']},
    {'pos': 4, 'team': 'ITECO', 'city': 'Н.Новгород', 'games': 1, 'w': 0, 'd': 1, 'l': 0, 'goals': '2-2', 'diff': '0', 'points': 1, 'form': ['D']},
    {'pos': 5, 'team': 'ФХНН-2', 'city': 'Н.Новгород', 'games': 1, 'w': 0, 'd': 1, 'l': 0, 'goals': '2-2', 'diff': '0', 'points': 1, 'form': ['D']},
    {'pos': 6, 'team': 'Красная Рамень', 'city': 'Останкино', 'games': 1, 'w': 0, 'd': 0, 'l': 1, 'goals': '3-5', 'diff': '-2', 'points': 0, 'form': ['L']},
    {'pos': 7, 'team': 'ННГУ им. Лобачевского', 'city': 'Н.Новгород', 'games': 1, 'w': 0, 'd': 0, 'l': 1, 'goals': '1-3', 'diff': '-2', 'points': 0, 'form': ['L']},
    {'pos': 8, 'team': 'Продтерминал', 'city': 'Н.Новгород', 'games': 1, 'w': 0, 'd': 0, 'l': 1, 'goals': '1-4', 'diff': '-3', 'points': 0, 'form': ['L']}
]

data = {
    'team_name': 'Доза Агро',
    'city': 'Нижний Новгород',
    'tournament': 'Первая лига-2026/2027',
    'sport': 'Мини-футбол (Футзал)',
    'tournament_url': 'https://nndepsport.nagradion.ru/tournament46746',
    'team_logo': team_logo,
    'team_photo': team_photo,
    'players': players,
    'coaches': coaches,
    'matches': matches,
    'standings': standings
}

with open('site_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Updated site_data.json successfully with complete data!')
