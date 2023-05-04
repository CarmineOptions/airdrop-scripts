from typing import Dict

import pandas as pd

from src.activity_allocation.activity_allocation import get_activity_allocation
from src.trade_based import get_traders_drop
from src.liq_based import get_liquidity_providers_drop
from src.community_projects.community_projects import get_community_projects


# Small note, the code is quite inefficient, but no need to worry about it right now



def get_core_team(period: str) -> Dict[str, int]:
    if period != 'week_1_4':
        raise ValueError
    return {'0x02af7135154dc27d9311b79c57ccc7b3a6ed74efd0c2b81116e8eb49dbf6aaf8': 83_333}


def get_token_distribution_week_1_4() -> Dict[str, int]:
    core_team_addresses = {
        '0x0583a9d956d65628f806386ab5b12dccd74236a3c6b930ded9cf3c54efc722a1',
        '0x583a9d956d65628f806386ab5b12dccd74236a3c6b930ded9cf3c54efc722a1',
        '0x06717eaf502baac2b6b2c6ee3ac39b34a52e726a73905ed586e757158270a0af',
        '0x6717eaf502baac2b6b2c6ee3ac39b34a52e726a73905ed586e757158270a0af',
        '0x0011d341c6e841426448ff39aa443a6dbb428914e05ba2259463c18308b86233',
        '0x011d341c6e841426448ff39aa443a6dbb428914e05ba2259463c18308b86233',
        '0x11d341c6e841426448ff39aa443a6dbb428914e05ba2259463c18308b86233',
        '0x03d1525605db970fa1724693404f5f64cba8af82ec4aab514e6ebd3dec4838ad',
        '0x3d1525605db970fa1724693404f5f64cba8af82ec4aab514e6ebd3dec4838ad',
        '0x03c032b19003Bdd6f4155a30FFFA0bDA3a9cAe45Feb994A721299d7E5096568c',
        '0x3c032b19003Bdd6f4155a30FFFA0bDA3a9cAe45Feb994A721299d7E5096568c',
    }
    week_1_end = 1681689600  # Mon Apr 17 2023 00:00:00 GMT+0000
    week_2_start = week_1_end
    week_3_start = week_2_start + 7 * 24 * 3600
    week_4_start = week_3_start + 7 * 24 * 3600
    week_5_start = week_4_start + 7 * 24 * 3600

    traders_1 = get_traders_drop(0, week_1_end, 125_000, core_team_addresses)
    traders_2 = get_traders_drop(week_2_start, week_3_start, 125_000, core_team_addresses)
    traders_3 = get_traders_drop(week_3_start, week_4_start, 125_000, core_team_addresses)
    traders_4 = get_traders_drop(week_4_start, week_5_start, 125_000, core_team_addresses)
    traders_total = {
        k: traders_1.get(k, 0) + traders_2.get(k, 0) + traders_3.get(k, 0) + traders_4.get(k, 0)
        for k in set(traders_1) | set(traders_2) | set(traders_3) | set(traders_4)
    }

    stakers_1 = get_liquidity_providers_drop(0, week_1_end, 125_000, True, core_team_addresses)
    stakers_2 = get_liquidity_providers_drop(week_2_start, week_3_start, 125_000, False, core_team_addresses)
    stakers_3 = get_liquidity_providers_drop(week_3_start, week_4_start, 125_000, False, core_team_addresses)
    stakers_4 = get_liquidity_providers_drop(week_4_start, week_5_start, 125_000, False, core_team_addresses)
    stakers_total = {
        k: stakers_1.get(k, 0) + stakers_2.get(k, 0) + stakers_3.get(k, 0) + stakers_4.get(k, 0)
        for k in set(stakers_1) | set(stakers_2) | set(stakers_3) | set(stakers_4)
    }

    # activity allocation and community projects works for the 4 weeks together
    activity_allocation = get_activity_allocation(
        trading_activity_addresses=list(set(traders_total)),
        staking_activity_addresses=list(set(stakers_total)),
        processed_OGs_filename='src/activity_allocation/processed_OGs.txt',
        processed_testnet_filename='src/activity_allocation/processed_testnet.txt',
        period='week_1_4'
    )

    community_projects = get_community_projects(period='week_1_4')

    # most of the team had the tokens distributed already
    core_team = get_core_team('week_1_4')

    # sum everything
    total_tokens = {
        k: traders_total.get(k, 0) + stakers_total.get(k, 0) + activity_allocation.get(k, 0) + community_projects.get(k, 0) + core_team.get(k, 0)
        for k in set(traders_total) | set(stakers_total) | set(activity_allocation) | set(community_projects) | set(core_team)
    }

    # there might be non-unified addresses
    df = pd.DataFrame({'address': total_tokens.keys(), 'tokens': total_tokens.values()})
    df.address = df.address.map(lambda x: hex(int(x, 0)))
    # manually rewrite some of the metamask addresses to Starknet addresses
    df.address = df.address.replace('0x2162FEB49E9Efe2506DE3273f4edabe09d36cbAf', '0x07657EEb175A5d3B51c5abFa2cd73B367da8F0Ebc4b3a7c1804F77e8b30b1ff4')

    total_tokens = df.groupby('address').tokens.sum().to_dict()

    # round down the tokens
    total_tokens = {address: int(tokens) for address, tokens in total_tokens.items()}

    return total_tokens
