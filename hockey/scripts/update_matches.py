#!/usr/bin/env python3
"""Uppdatera verifierade svenska gruppspelsmatcher i herr-VM 2027 från IIHF Hydra.
Avsiktligt fail-closed: andra lag och turneringar kräver egna källadaptrar.
"""
import datetime as dt
import json
import os
import pathlib
import re
import sys
from zoneinfo import ZoneInfo

import requests
from bs4 import BeautifulSoup

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'matches.json'
SOURCE = 'https://stats.iihf.com/Hydra/985/index.html'
TEAMS = {'SWE':'Sverige','UKR':'Ukraina','LAT':'Lettland','SLO':'Slovenien',
         'AUT':'Österrike','SUI':'Schweiz','FIN':'Finland','GER':'Tyskland'}
SWEDEN = ZoneInfo('Europe/Stockholm')
# Expected known matches: fail rather than silently publish incomplete parsing.
EXPECTED = {'2027-05-14','2027-05-16','2027-05-17','2027-05-20',
            '2027-05-21','2027-05-23','2027-05-25'}

def parse_schedule(html):
    soup = BeautifulSoup(html, 'html.parser')
    result = {}
    current_date = None
    # Hydra table generally puts a date heading on a row preceding its fixtures.
    for row in soup.select('tr'):
        text = ' '.join(row.stripped_strings)
        date_match = re.search(r'\b(\d{1,2})\s+May\s+2027\b', text, re.I)
        if date_match:
            current_date = f'2027-05-{int(date_match.group(1)):02d}'
        if not current_date or not re.search(r'\bSWE\b', text):
            continue
        # Only read explicit schedule rows, not standings or unrelated links.
        team_match = re.search(r'\b(UKR|LAT|SLO|AUT|SUI|FIN|GER|SWE)\s*[-–]\s*(UKR|LAT|SLO|AUT|SUI|FIN|GER|SWE)\b', text)
        clock_match = re.search(r'\b([012]?\d:[0-5]\d)\b', text)
        if not team_match or not clock_match:
            continue
        home,away = team_match.groups()
        if home != 'SWE' and away != 'SWE':
            continue
        clock = clock_match.group(1).zfill(5)
        # The IIHF Hydra 2027 event lists local CEST (GMT+2) match starts.
        instant = dt.datetime.fromisoformat(current_date + 'T' + clock).replace(tzinfo=SWEDEN)
        result[current_date] = {'date':current_date, 'time':clock,
                                 'home':TEAMS[home], 'away':TEAMS[away],
                                 'startUtc':instant.astimezone(dt.timezone.utc).isoformat().replace('+00:00','Z')}
    return result

def main():
    response = requests.get(SOURCE,timeout=35,headers={'User-Agent':'TreKronorMatchcenter/1.0 (public schedule checker)'})
    response.raise_for_status()
    found = parse_schedule(response.text)
    if not EXPECTED.issubset(set(found)):
        raise RuntimeError(f'IIHF-formatet ändrat eller matchdata ofullständig ({len(found)}/7). Behåller tidigare data.')
    data = json.loads(DATA.read_text(encoding='utf-8'))
    selected = [m for m in data['matches'] if m['tournament']=='Herr-VM 2027' and m['category']=='herr']
    if len(selected) != 7:
        raise RuntimeError('Förväntade 7 VM-matcher i den lokala matchfilen. Inga ändringar sparade.')
    # Preserve stable IDs using opponent; reject surprising rearrangements for manual review.
    existing = {(m['home'],m['away']):m for m in selected}
    incoming = {(m['home'],m['away']):m for m in found.values()}
    if set(existing) != set(incoming):
        raise RuntimeError('Motståndare/hemma-borta ändrat i IIHF – kräver manuell granskning.')
    changes = 0
    for key,new in incoming.items():
        old = existing[key]
        for field in ('date','time','startUtc'):
            if old[field] != new[field]:
                old[field] = new[field]
                changes += 1
        old['sourceStatus'] = 'IIHF kontrollerad automatiskt'
    # Do not rewrite data for unchanged checks, to avoid unnecessary deployments.
    # Store successful check timestamp separately only when changed OR first success.
    if changes or not data.get('sourceCheckedAt'):
        data['sourceCheckedAt'] = dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z')
        DATA.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'IIHF-kontroll OK. {len(found)} matcher; {changes} ändrade fält.')

if __name__=='__main__':
    try:main()
    except Exception as exc:
        print('INGA ÄNDRINGAR GJORDA:',exc,file=sys.stderr)
        sys.exit(1)
