from typing import Dict
import json
import decimal
import os

import pandas as pd

from trade_based import get_traders_drop
from liq_based import get_liquidity_providers_drop
from vote_based import get_vote_tokens


def get_token_distribution_round_4() -> Dict[str, int]:

    # Community Projects
    ammbasodors_and_moderators = {}
    investors = {}
    point_based = {}
    community_developers = {}
    zealy_users = {}
    galxe_users = {}
    gitcoin_contributors = {}
    poolcleaners = {}


    # Core Team
    core_team = {
        '0x0011d341c6e841426448ff39aa443a6dbb428914e05ba2259463c18308b86233' : 100_000,
        '0x0583a9d956d65628f806386ab5b12dccd74236a3c6b930ded9cf3c54efc722a1' : 40_000, 
        '0x03d1525605db970fa1724693404f5f64cba8af82ec4aab514e6ebd3dec4838ad' : 30_000, 
        '0x06717eaf502baac2b6b2c6ee3ac39b34a52e726a73905ed586e757158270a0af' : 30_000, 
        '0x06fd0529AC6d4515dA8E5f7B093e29ac0A546a42FB36C695c8f9D13c5f787f82' : 5_000,  
    }

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
        '0x6fd0529ac6d4515da8e5f7b093e29ac0a546a42fb36c695c8f9d13c5f787f82',
    }

    # Activity Allocation
    starkscan_api_key = os.getenv('STARKSCAN_API_KEY')
    if starkscan_api_key is None:
        raise SystemExit(f'STARKSCAN_API_KEY env not provided. Exiting...')


    # Traders - 200_000 - 50_000/week
    # There are 50_000 tokens distributed each week for traders. The function takes half (25_000) of
    # it as an argument, because it distributes the passed value in call and put pool separately,
    # so 50_000 in total
    traders_1 = get_traders_drop(week_9_start,  week_10_start, 25_000, core_team_addresses)
    traders_2 = get_traders_drop(week_10_start, week_11_start, 25_000, core_team_addresses)
    traders_3 = get_traders_drop(week_11_start, week_12_start, 25_000, core_team_addresses)
    traders_4 = get_traders_drop(week_12_start, week_12_end,   25_000, core_team_addresses)
    traders_total = {
        k: traders_1.get(k, 0) + traders_2.get(k, 0) + traders_3.get(k, 0) + traders_4.get(k, 0)
        for k in set(traders_1) | set(traders_2) | set(traders_3) | set(traders_4)
    }

    # Stakers - 150_000 - 37_500/week
    # There are 37_500 tokens distributed each week. The function takes half (18_750) of
    # it as an argument, because it distributes the passed value in call and put pool separately,
    # so 37_500 in total
    stakers_1 = get_liquidity_providers_drop(week_9_start,  week_10_start, 18_750, False, core_team_addresses)
    stakers_2 = get_liquidity_providers_drop(week_10_start, week_11_start, 18_750, False, core_team_addresses)
    stakers_3 = get_liquidity_providers_drop(week_11_start, week_12_start, 18_750, False, core_team_addresses)
    stakers_4 = get_liquidity_providers_drop(week_12_start, week_12_end,   18_750, False, core_team_addresses)
    stakers_total = {
        k: stakers_1.get(k, 0) + stakers_2.get(k, 0) + stakers_3.get(k, 0) + stakers_4.get(k, 0)
        for k in set(stakers_1) | set(stakers_2) | set(stakers_3) | set(stakers_4)
    }

    print(f"\n\033[94mTotal distributed for staking:\033[0m {sum(stakers_total.values()):_}")
    print(f"\033[94mTotal distributed for trading:\033[0m {sum(traders_total.values()):_}")
    print(f"\033[94mTotal distributed for community projects:\033[0m {sum(community_projects.values()):_}")
    print(f"\033[94mTotal distributed for activity allocation:\033[0m {sum(activity_allocation.values()):_}")
    print('\n')
    print(
        f"""\033[93mTotal distributed to community:\033[0m {
                sum(stakers_total.values()) + 
                sum(traders_total.values()) +  
                sum(community_projects.values()) + 
                sum(activity_allocation.values()):_}"""
    )
    print(f"\033[93mTotal distributed to core team:\033[0m {sum(core_team.values()):_}")

    # Normalize the addresses before summing up so that no values are lost
    traders_total       = {hex(int(key, 0)): value for key, value in traders_total.items()}
    stakers_total       = {hex(int(key, 0)): value for key, value in stakers_total.items()}
    community_projects  = {hex(int(key, 0)): value for key, value in community_projects.items()}
    activity_allocation = {hex(int(key, 0)): value for key, value in activity_allocation.items()}
    core_team           = {hex(int(key, 0)): value for key, value in core_team.items()}

    # Sum everything
    total_tokens = {
        k: traders_total.get(k, 0) +
           stakers_total.get(k, 0) +
           activity_allocation.get(k, 0) +
           community_projects.get(k, 0) +
           core_team.get(k, 0)
        for k in set(traders_total) | set(stakers_total) | set(activity_allocation) | set(community_projects) | set(core_team)
    }
    print(f"\033[93mTotal distributed in third round:\033[0m {sum(total_tokens.values()):_}")

    # Round down the tokens
    def _adjust_tokens_number(tokens: float) -> str:
        raw_number_of_tokens = decimal.Decimal(str(tokens)) * decimal.Decimal(10**18)
        rounded_number_of_tokens = raw_number_of_tokens.quantize(
            decimal.Decimal('1.'),
            rounding=decimal.ROUND_DOWN
        )
        return rounded_number_of_tokens.to_eng_string()


    # https://github.com/CarmineOptions/carmine-api/blob/master/carmine-api-airdrop/src/air-drop.json
    # template for the json
    third_dist = {
        address: _adjust_tokens_number(tokens)
        for address, tokens in total_tokens.items()
    }


    # Uncomment this part to save prelims to csv
    res_df = pd.DataFrame({'address': third_dist.keys(), 'tokens': third_dist.values()})
    res_df['tokens'] = res_df['tokens'].map(lambda x: int(x) / 10 ** 18)
    res_df = res_df.sort_values('tokens', ascending = False)
    res_df.to_csv("prelim_round_4.csv", index = False)
    
    # Load second distribution
    with open('second_distribution_calculated.json', 'r') as infile:
        fourth_dist = {
            x['address']: x['amount'] for x in json.load(infile)
        }


    # Combine current airdrop with previous
    total_tokens_combined = {
        k: int(second_dist.get(k, 0)) + int(third_dist.get(k, 0)) + int(fourth_dist.get(k, 0))
        for k in set(second_dist) | set(third_dist) | set(fourth_dist)
    }
    print(f"\033[93mTotal distributed in three rounds:\033[0m {sum(total_tokens_combined.values()) / 10**18:_}")


    # Assert that there is truly no non-normalized address
    non_normalized = [
        addr for addr in list(total_tokens_combined.keys()) if '0x0' in addr
    ]
    if non_normalized:
        raise ValueError(f"Some addresses are not normalized:\n {non_normalized}")


    final_json = [
        {'address': address, 'amount': val}
        for address, val in total_tokens_combined.items()
    ]

    open('third_distribution_calculated.json', 'w+').write(json.dumps(final_json))


if __name__ == '__main__':
    get_token_distribution_week_9_12()
