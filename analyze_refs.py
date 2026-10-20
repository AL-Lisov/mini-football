import re
import os
import sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

def analyze_file(pattern, label):
    files = [f for f in os.listdir('.') if pattern in f]
    if not files:
        print(f'No file matching {pattern}')
        return
    fname = files[0]
    print(f'\n========================================')
    print(f'ANALYZING: {label} ({fname[:40]}...)')
    print(f'========================================')
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    print('Length:', len(html))
    
    # Fonts
    fonts = re.findall(r'font-family:\s*([^;\}]+)', html, re.I)
    f_counts = Counter([f.strip() for f in fonts])
    print('\nTop fonts:')
    for font, count in f_counts.most_common(5):
        print(f'  {font}: {count}')

    # Border radius
    radii = re.findall(r'border-radius:\s*([^;\}]+)', html, re.I)
    r_counts = Counter([r.strip() for r in radii])
    print('\nTop border-radius:')
    for r, count in r_counts.most_common(8):
        print(f'  {r}: {count}')

    # Hex colors
    colors = re.findall(r'#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b', html)
    c_counts = Counter([c.lower() for c in colors])
    print('\nTop hex colors:')
    for c, count in c_counts.most_common(12):
        print(f'  #{c}: {count}')

    # Sample components or classes
    classes = re.findall(r'class=["\']([^"\']+)["\']', html)
    all_classes = []
    for cls_str in classes:
        all_classes.extend(cls_str.split())
    cls_counts = Counter(all_classes)
    print('\nTop classes:')
    for cl, count in cls_counts.most_common(15):
        print(f'  .{cl}: {count}')

analyze_file('Суперлига', 'SUPERLIGA RFS')
analyze_file('Т-Банк', 'T-BANK')
