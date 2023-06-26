from typing import Dict
import json
import decimal

import pandas as pd

from trade_based import get_traders_drop
from liq_based import get_liquidity_providers_drop

# Traders - 312 500 - 78_125/week
# Stakers - 312 500 - 78_125/week

# Community Projects
    # Marek's Discretion
    # 0x047991fc342a58b8446c7265b1657aa169ce0323b275dab0a06c8961bf481b37 - 5_000 Carms - reported oracle bug

    # Mods - 15_000
    # ???

    # Community Devs - 30_000
    # '0x486deba6028c880ce3d1730a4496e4f12d7b813367d43510ea410f5ff7e3efb' : 15_000, 
    # '0x365421f66a3fb7630ac030fb83a1db5078bfe29cc22f27f95a9978ff9ab7b6e' : 15_000, 
    
    # Alternative FE - 30_000 ???

# Activity Allocation
    # Voting in Proposals - 25_000

# Core - half of what community gets

def get_token_distribution_week_9_12() -> Dict[str, int]:

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
        '0x03c032b19003bdd6f4155a30fffa0bda3a9cae45feb994a721299d7e5096568c',
        '0x3c032b19003bdd6f4155a30fffa0bda3a9cae45feb994a721299d7e5096568c',
        '0x02af7135154dc27d9311b79c57ccc7b3a6ed74efd0c2b81116e8eb49dbf6aaf8',
        '0x2af7135154dc27d9311b79c57ccc7b3a6ed74efd0c2b81116e8eb49dbf6aaf8',
        '0x06fd0529ac6d4515da8e5f7b093e29ac0a546a42fb36c695c8f9d13c5f787f82',
        '0x6fd0529ac6d4515da8e5f7b093e29ac0a546a42fb36c695c8f9d13c5f787f82' 
    }

    week_9_start = 1685923200 # Mon Jun 05 2023 00:00:00 GMT+0000
    week_10_start = week_9_start + 7 * 24 * 3600
    week_11_start = week_10_start + 7 * 24 * 3600
    week_12_start = week_11_start + 7 * 24 * 3600
    week_12_end = week_12_start + 7 * 24 * 3600 

    # There are 78 125 tokens distributed each week. The function takes half (39 062.5) of
    # it as an argument, because it distributes the passed value in call and put pool separately,
    # so 78 125 in total
    traders_1 = get_traders_drop(week_9_start,  week_10_start, 39_062.5, core_team_addresses)
    traders_2 = get_traders_drop(week_10_start, week_11_start, 39_062.5, core_team_addresses)
    traders_3 = get_traders_drop(week_11_start, week_12_start, 39_062.5, core_team_addresses)
    traders_4 = get_traders_drop(week_12_start, week_12_end,   39_062.5, core_team_addresses)
    traders_total = {
        k: traders_1.get(k, 0) + traders_2.get(k, 0) + traders_3.get(k, 0) + traders_4.get(k, 0)
        for k in set(traders_1) | set(traders_2) | set(traders_3) | set(traders_4)
    }

    # There are 78 125 tokens distributed each week. The function takes half (39 062.5) of
    # it as an argument, because it distributes the passed value in call and put pool separately,
    # so 78 125 in total
    stakers_1 = get_liquidity_providers_drop(week_9_start,  week_10_start, 39_062.5, False, core_team_addresses)
    stakers_2 = get_liquidity_providers_drop(week_10_start, week_11_start, 39_062.5, False, core_team_addresses)
    stakers_3 = get_liquidity_providers_drop(week_11_start, week_12_start, 39_062.5, False, core_team_addresses)
    stakers_4 = get_liquidity_providers_drop(week_12_start, week_12_end,   39_062.5, False, core_team_addresses)
    stakers_total = {
        k: stakers_1.get(k, 0) + stakers_2.get(k, 0) + stakers_3.get(k, 0) + stakers_4.get(k, 0)
        for k in set(stakers_1) | set(stakers_2) | set(stakers_3) | set(stakers_4)
    }
    


