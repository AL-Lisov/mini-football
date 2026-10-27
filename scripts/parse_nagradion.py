#!/usr/bin/env python3
"""
Скрипт для парсинга протоколов матчей и турнирной таблицы МФК «Доза Агро»
с портала «Наградион» (Первая лига Чемпионата города).
"""

import sys
import re
import json
import urllib.request

TOURNAMENT_ID = "46746"
TEAM_ID = "696688"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def fetch_url(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req) as resp:
        return resp.read().decode("utf-8", errors="replace")

def parse_match(match_id):
    url = f"https://nndepsport.nagradion.ru/tournament{TOURNAMENT_ID}/match/{match_id}"
    html = fetch_url(url)
    
    score_match = re.search(r'class="score[^"]*"[^>]*>\s*(\d+)\s*:\s*(\d+)', html)
    score = f"{score_match.group(1)} : {score_match.group(2)}" if score_match else "N/A"
    
    events = re.findall(r'class="event-name"[^>]*>([^<]+)</span>.*?class="player-name"[^>]*>([^<]+)</a>', html, re.DOTALL)
    
    return {
        "match_id": match_id,
        "url": url,
        "score": score,
        "events": events
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        match_id = sys.argv[1]
        data = parse_match(match_id)
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print("Использование: python parse_nagradion.py <match_id>")
