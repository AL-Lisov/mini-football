import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

files = [f for f in os.listdir('.') if f.endswith('.html') and 'Департамент' in f]
if not files:
    print('No file found')
    exit()

fname = files[0]
print(f'Analyzing SingleFile html...')


with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

print('Length:', len(html))

# Extract title
title = re.search(r'<title>(.*?)</title>', html, re.I | re.DOTALL)
print('Title:', title.group(1).strip() if title else '')

# Extract colors (hex colors)
hex_colors = re.findall(r'#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b', html)
from collections import Counter
c_counts = Counter([c.lower() for c in hex_colors])
print('Top 20 hex colors:')
for color, count in c_counts.most_common(20):
    print(f'  #{color}: {count}')

# Extract background colors in styles
bg_styles = re.findall(r'background(?:-color)?:\s*([^;]+);', html, re.I)
bg_counts = Counter([b.strip().lower() for b in bg_styles])
print('\nTop 15 backgrounds:')
for bg, count in bg_counts.most_common(15):
    print(f'  {bg}: {count}')

# Extract logos
logos = re.findall(r'<img[^>]+(?:logo|shield|brand|header)[^>]+>', html, re.I)
print(f'\nFound {len(logos)} logo/header images:')
for l in logos[:5]:
    print(' ', l[:150])

# Extract header text or navbar
navbar = re.findall(r'<header[^>]*>.*?</header>', html, re.I | re.DOTALL)
print(f'\nHeaders count: {len(navbar)}')
