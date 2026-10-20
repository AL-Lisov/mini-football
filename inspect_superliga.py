import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('БЕТСИТИ Суперлига 2026_27 ｜ Чемпионат России по футзалу (20.10.2026 11：26：56).html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Find team names and tournament widgets
tourn_matches = re.findall(r'<div[^>]*class=["\'][^"\']*tournamentswidget[^"\']*["\'][^>]*>(.*?)</div>\s*</div>', text, re.DOTALL)
print('Tournaments widgets found:', len(tourn_matches))

# Look for tteams classes
team_matches = re.findall(r'<div[^>]*class=["\'][^"\']*tteams[^"\']*["\'][^>]*>(.*?)</div>', text, re.DOTALL)
print('Team blocks found:', len(team_matches))

# Check table snippet
for t in team_matches[:5]:
    cleaned = re.sub(r'<[^>]+>', ' ', t)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    if cleaned:
        print('  Snippet:', cleaned[:150])
