from typing import Dict
import json
import decimal
import os

import pandas as pd

from trade_based import get_traders_drop
from liq_based import get_liquidity_providers_drop
from vote_based import get_vote_tokens

def get_token_distribution_week_9_12() -> Dict[str, int]:

    week_9_start = 1685923200 # Mon Jun 05 2023 00:00:00 GMT+0000
    week_10_start = week_9_start + 7 * 24 * 3600
    week_11_start = week_10_start + 7 * 24 * 3600
    week_12_start = week_11_start + 7 * 24 * 3600
    week_12_end = week_12_start + 7 * 24 * 3600 # Mon Jul 03 2023 00:00:00 GMT+0000

    # Community Projects
    community_projects = {
        # Marek's Discretion
        # Ambassadors - 16_000
        '0x030c3f654Ead1da0c9166d483d3dd436dcbB57Ce8E1AdaA129995103A8dcCA4D': 8_000, 
        '0x01fb62ac54f9fa99e1417f83bcb88485556427397f717ed4e7233bc99be31bff': 8_000, 
        '0x037080eb7d9ff1f71c143fa5ea125850756439af288982f828230835482708f9': 1_500, 
        '0x068C8E344aBF736892a97daC9a3daF2952A047b769E085D7557901Ddf31a435f': 3_000, 

        # Mods - 1500 each  
        '0x04d2FE1Ff7c0181a4F473dCd982402D456385BAE3a0fc38C49C0A99A620d1abe' : 1_500,
        '0x039e14d815587cdd5ae400684e5d60848d9a134b378260cc1f2de6e7aedcdb45' : 1_500,
        '0x0639f7ad800fcbe2ad56e3b000f9a0581759cce989b3ee09477055c0816a12c7' : 1_500,
        '0x006a0f490289fe04ea6ba158ed5fd3339628832432d7bc802941664843bc904f' : 1_500,
        '0x04d3E6A312d4089Ac798Ae3Cf5766AdB1c1863E23222B5602F19682E08DB2Bd1' : 1_500,
        '0x0508350Eef9c741692cFb2882B7c0d6E2639C589c667ee0b10E08A2Ab7f256f5' : 1_500,
        '0x053eAD44Bb90853003d70E6930000Ef8C4a4819493fDC8f1CbdC1282121498eC' : 1_500,

        # Community devs - 30_000
        '0x486deba6028c880ce3d1730a4496e4f12d7b813367d43510ea410f5ff7e3efb' : 15_000, 
        '0x365421f66a3fb7630ac030fb83a1db5078bfe29cc22f27f95a9978ff9ab7b6e' : 15_000, 
    }

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
    
    tokens_dist_for_voting = 25_000

    # Voting in Proposals - 25_000
    activity_allocation = get_vote_tokens(
        api_key = starkscan_api_key, 
        time_start = week_9_start,
        time_end = week_12_end,
        to_distribute = tokens_dist_for_voting,
        core_team_addresses = core_team_addresses
    )


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
    # res_df = pd.DataFrame({'address': third_dist.keys(), 'tokens': third_dist.values()})
    # res_df['tokens'] = res_df['tokens'].map(lambda x: int(x) / 10 ** 18)
    # res_df = res_df.sort_values('tokens', ascending = False)
    # res_df.to_csv("prelim_round_3.csv", index = False)
    
    # Load second distribution
    with open('second_distribution_calculated.json', 'r') as infile:
        second_dist = {
            x['address']: x['amount'] for x in json.load(infile)
        }


    # Combine current airdrop with previous
    total_tokens_combined = {
        k: int(second_dist.get(k, 0)) + int(third_dist.get(k, 0))
        for k in set(second_dist) | set(third_dist)
    }
    print(f"\033[93mTotal distributed in three rounds:\033[0m {sum(total_tokens_combined.values()) / 10**18:_}")


    # Assert that there is truly no non-normalized address
    non_normalized = [
        addr for addr in list(total_tokens_combined.keys()) if '0x0' in addr
    ]
    if non_normalized:
        raise ValueError(f"Some addresses are not normalized:\n {non_normalized}")


    final_json = []
    for address, val in total_tokens_combined.items():
        final_json.append({'address': address, 'amount': val})

    open('third_distribution_calculated.json', 'w+').write(json.dumps(final_json))


if __name__ == '__main__':
    get_token_distribution_week_9_12()
