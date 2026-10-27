import urllib.request
import re
import json

url = 'https://nndepsport.nagradion.ru/tournament46746/team/448703/players'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
with urllib.request.urlopen(req) as resp:
    raw = resp.read()
    charset = resp.headers.get_content_charset() or 'utf-8'
    text = raw.decode(charset, errors='replace')

print('Encoding:', charset)
print('Length in chars:', len(text))

# Check viewport
viewports = re.findall(r'<meta[^>]*viewport[^>]*>', text, re.I)
print('Viewport tags:', viewports)

# Check CSS
css_links = re.findall(r'<link[^>]*rel=["\']stylesheet["\'][^>]*>', text, re.I)
print('\nCSS links count:', len(css_links))
for c in css_links:
    print('  CSS:', c)

# Check Bootstrap or framework
print('\nBootstrap/Grid mentions:')
for framework in ['bootstrap', 'tailwind', 'foundation', 'uikit', 'react', 'vue', 'jquery']:
    matches = re.findall(framework, text, re.I)
    if matches:
        print(f'  Found {framework}: {len(matches)} times')

# Check tables
tables = re.findall(r'<table[^>]*>', text, re.I)
print('\nTables count:', len(tables))
for t in tables[:10]:
    print('  Table:', t)

# Inspect main structure
# Let's see what layout sections exist
sections = re.findall(r'<div[^>]*class=["\']([^"\']+)["\']', text, re.I)
unique_classes = set()
for s in sections:
    for cls in s.split():
        unique_classes.add(cls)

print('\nTotal unique classes:', len(unique_classes))
relevant = [c for c in unique_classes if any(k in c.lower() for k in ['grid', 'col-', 'table', 'player', 'team', 'match', 'menu', 'sidebar', 'nav', 'header', 'footer'])]
print('Sample relevant classes:', sorted(relevant)[:40])

# Inspect matches & players structure
players = re.findall(r'/tournament\d+/player/\d+', text)
print('\nPlayer profile links count:', len(players))

matches = re.findall(r'/tournament\d+/match/\d+', text)
print('Match links count:', len(matches))
