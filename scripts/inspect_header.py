import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

fname = [f for f in os.listdir('.') if f.endswith('.html') and 'Департамент' in f][0]

with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# Let's inspect the top header and banner
# Search for Департамент in html
matches = [m.start() for m in re.finditer(r'Департамент', html)]
print('Matches count for Департамент:', len(matches))
for idx in matches[:3]:
    print('--- MATCH ---')
    print(html[max(0, idx-100):min(len(html), idx+300)])

# Check navigation menu links on main page
nav_links = re.findall(r'<a[^>]+href="([^"]+)"[^>]*>([^<]+)</a>', html[:50000])
print('\nTop nav links count:', len(nav_links))
for href, text in nav_links[:15]:
    if text.strip():
        print(f'  {text.strip()} -> {href}')
