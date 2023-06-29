import requests
import time

import pandas as pd

GOV_ADDR = '0x001405ab78ab6ec90fba09e6116f373cda53b0ba557789a4578d8c1ec374ba0f'
EVENTS_URL = f'https://api.starkscan.co/api/v0/events?from_address={GOV_ADDR}&limit=100'

def get_vote_events(api_key):
    print('Fetching governance vote events')

    resps = []

    headers = {
        "accept": "application/json",
        "x-api-key": api_key,
    }

    url = EVENTS_URL

    while True:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        resps.extend(response.json()['data'])
        url = response.json()['next_url']
        if not url:
            break
        time.sleep(0.1)
    vote_events = [i for i in resps if i['key_name'] == 'Voted']

    return vote_events

def get_vote_tokens(api_key, time_start, time_end, to_distribute, core_team_addresses):
    votes = get_vote_events(api_key)
    
    votes = pd.DataFrame(votes)
    votes = votes[(votes['timestamp'] >= time_start) & (votes['timestamp'] <= time_end)]
    votes['voter'] = [i[1] for i in votes['data']]

    # Normalize addresses
    votes['voter'] = votes['voter'].apply(lambda x: hex(int(x, 0)))

    # Remove entries from core team
    # But first normalize core_team_addresses as well
    core_team_addresses = {hex(int(x, 0)) for x in core_team_addresses}
    votes = votes[~votes['voter'].isin(core_team_addresses)]

    counts = votes[['voter']].value_counts().reset_index()
    counts.columns = ['address', 'vote_count']
    counts['vote_ratio'] = counts['vote_count'] / counts['vote_count'].sum()
    counts['tokens'] = counts['vote_ratio'] * to_distribute

    counts = counts[['address', 'tokens']]
    counts['tokens'] = counts['tokens'].map(lambda x: int(x))
    counts = counts.set_index('address').to_dict()['tokens']

    return counts

