import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Let's inspect Superliga match ticker
with open('БЕТСИТИ Суперлига 2026_27 ｜ Чемпионат России по футзалу (20.10.2026 11：26：56).html', 'r', encoding='utf-8', errors='ignore') as f:
    rfs_html = f.read()

# Look for match cells
print('--- RFS MATCH TICKER SAMPLE ---')
match_chunk = re.search(r'(<div[^>]*blk-tournamentswidget__cell--team-1.*?</div>\s*</div>\s*</div>)', rfs_html, re.DOTALL)
if match_chunk:
    print(match_chunk.group(1)[:600])

# Look for player roster in RFS
print('\n--- RFS PLAYER ROSTER SAMPLE ---')
player_chunk = re.search(r'(<div[^>]*blk-tteams__cell--number.*?</div>\s*</div>)', rfs_html, re.DOTALL)
if player_chunk:
    print(player_chunk.group(1)[:600])
