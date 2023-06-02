
from typing import Dict
import json
import decimal

import pandas as pd

from trade_based import get_traders_drop
from liq_based import get_liquidity_providers_drop



'''
Increase tokens of these guys

    df.address = df.address.replace(
        '0x2162FEB49E9Efe2506DE3273f4edabe09d36cbAf'.lower(),
        '0x7657EEb175A5d3B51c5abFa2cd73B367da8F0Ebc4b3a7c1804F77e8b30b1ff4'.lower()
    )
    df.address = df.address.replace(
        '0x271933d1DAFFEC39E1E8c805DbAFf4e10eCd00BB'.lower(),
        '0x6E7B39f21c1A73A2a266A2A60Ac7FDA4AFE6EbE575bA489c87F68A419EdcA81'.lower()
    )
    df.address = df.address.replace(
        '0x5025917a621e5CD46824350ba98F9766160d84BC'.lower(),
        '0x27495304ed75F5257EC68e053e13B4B842Ec9AE65b4720e2EE88b31ecC37A71'.lower()
    )
there was a bug in the contributions... 
df = df[df['Mainnet (StarkNet) address'].map(len) > 42]
was used before the replacement - HOW MUCH?
'''

'''
give some tokens to puddington#8374, he was doing the sybil filtering for airdrop 1, for the tweets - Marek doda
'''


'''
Each of these get 500 Carmine Tokens... thanks to campaign with https://twitter.com/Starknet_Allday

@0xygenXT - Wait for correct address
: 0x031ac74fe11e3e083513671ebc4f98fac55fe045c0b7229cc74c8a1ae96f1273

@panda840z
:0x07d5851e60a1Ea9BcA3868070eB34C65395c43eD5cF4b96be0310853994184b1 

@Buduhun7
:
0x066463F57b5DE66dF56cf4774e5C6784e70Bbe9b333E9F1339D564A691459193
'''

'''
https://github.com/CarmineOptions/carmine-protocol/commit/c513ec2c672c10c13f50ecece0cd216c6493cfcc#diff-770ea621de180501274b95ab5d6ac3225b418be5801a8e10bc11210d6f0250f7R8
has to be updated... ie user can claim "get_eligible_amount minus airdrop_claimed"
'''

'''
the json generated from this script will collect both the numbers already written into smart contract
(first_distribution_calculated.json) plus the numbers from this script
'''

'''
periods end with 4th June -> 5th June there will be proposal for the distribution
'''

'''
watch out for tokens, since int is not precise enough... so you have to use decimals

# Additional tokens:
# александр gets 3kCARM to  wallet 0x068C8E344aBF736892a97daC9a3daF2952A047b769E085D7557901Ddf31a435f... for sharing info about us in his discord (roughly 12k followers, looks like interesting engagement, good feedback)
 
Our team - HOW MUCH?
Presto - HOW MUCH?
'''

def get_token_distribution_week_5_8() -> Dict[str, int]:
    # In total, this airdrop distributes 68_000 for community projects. After previous round there was 136_000
    # left, so after this airdrop there will be only 68_000 left
    community_projects = {
        # Mods - 7_500 of these goes from "Marek's discretion" and some numbers are high, because 
        # not everything was distributed during previous airdrop
        '0x04d2FE1Ff7c0181a4F473dCd982402D456385BAE3a0fc38C49C0A99A620d1abe' : 1_500, # Cryptowild
        '0x039e14d815587cdd5ae400684e5d60848d9a134b378260cc1f2de6e7aedcdb45' : 3_000, # PoolCleaner
        '0x0639f7ad800fcbe2ad56e3b000f9a0581759cce989b3ee09477055c0816a12c7' : 10_500,# JioJiu
        '0x006a0f490289fe04ea6ba158ed5fd3339628832432d7bc802941664843bc904f' : 4_500, # Black Kisat
        '0x04d3E6A312d4089Ac798Ae3Cf5766AdB1c1863E23222B5602F19682E08DB2Bd1' : 4_500, # Deliricee
        '0x0508350Eef9c741692cFb2882B7c0d6E2639C589c667ee0b10E08A2Ab7f256f5' : 6_000, # JiraYa_Og
        '0x053eAD44Bb90853003d70E6930000Ef8C4a4819493fDC8f1CbdC1282121498eC' : 1_500, # Okinawa

        # Marek's discretion
        '0x068C8E344aBF736892a97daC9a3daF2952A047b769E085D7557901Ddf31a435f' : 3_000, # Alexandr
        '0x055E0e6BbB31B295f9c11bDe85Fc1fB425bF1e1A86497dF4364AD862697705C9' : 2_000, # Puddington
        '0x07d5851e60a1Ea9BcA3868070eB34C65395c43eD5cF4b96be0310853994184b1' : 500,   # panda840z
        '0x066463F57b5DE66dF56cf4774e5C6784e70Bbe9b333E9F1339D564A691459193' : 500,   # Buduhun7
        '0x031ac74fe11e3e083513671ebc4f98fac55fe045c0b7229cc74c8a1ae96f1273' : 500,   # 0xygenXT 

        # Community Devs 
        '0x486deba6028c880ce3d1730a4496e4f12d7b813367d43510ea410f5ff7e3efb': 15_000, # Dev 1
        '0x365421f66a3fb7630ac030fb83a1db5078bfe29cc22f27f95a9978ff9ab7b6e': 15_000, # Dev 2
    }

    activity_allocation = {
        # Tokens that were supposed to be distributed in previous airdrop but weren't
        '0x7657EEb175A5d3B51c5abFa2cd73B367da8F0Ebc4b3a7c1804F77e8b30b1ff4' : 5970.1492537313439, # Some rando
        '0x6E7B39f21c1A73A2a266A2A60Ac7FDA4AFE6EbE575bA489c87F68A419EdcA81' : 1492.5373134328356, # Some rando
        '0x27495304ed75F5257EC68e053e13B4B842Ec9AE65b4720e2EE88b31ecC37A71' : 2238.805970149254   # Some rando
    }

    core_team = {
        # Core core
        '0x0011d341c6e841426448ff39aa443a6dbb428914e05ba2259463c18308b86233' : 100_000,# Marek
        '0x0583a9d956d65628f806386ab5b12dccd74236a3c6b930ded9cf3c54efc722a1' : 40_000, # Ondra
        '0x03d1525605db970fa1724693404f5f64cba8af82ec4aab514e6ebd3dec4838ad' : 30_000, # David
        '0x06717eaf502baac2b6b2c6ee3ac39b34a52e726a73905ed586e757158270a0af' : 30_000, # Andrej
        '0x06fd0529AC6d4515dA8E5f7B093e29ac0A546a42FB36C695c8f9D13c5f787f82' : 55_000, # Katsu
        # Note: Philip doesn't get anything this round as he received a lot previously

        # Core not so core
        '0x2af7135154dc27d9311b79c57ccc7b3a6ed74efd0c2b81116e8eb49dbf6aaf8'  : 83_333, # UX/UI Guy
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
        '0x6fd0529ac6d4515da8e5f7b093e29ac0a546a42fb36c695c8f9d13c5f787f82' 
    }

    week_5_start = 1683504000 # Mon May 08 2023 00:00:00 GMT+0000
    week_6_start = week_5_start + 7 * 24 * 3600
    week_7_start = week_6_start + 7 * 24 * 3600
    week_8_start = week_7_start + 7 * 24 * 3600
    week_8_end = week_8_start + 7 * 24 * 3600

    # There are 78 125 tokens distributed each week. The function takes half (39 062.5) of
    # it as an argument, because it distributes the passed value in call and put pool separately,
    # so 78 125 in total
    traders_1 = get_traders_drop(week_5_start, week_6_start, 39_062.5, core_team_addresses)
    traders_2 = get_traders_drop(week_6_start, week_7_start, 39_062.5, core_team_addresses)
    traders_3 = get_traders_drop(week_7_start, week_8_start, 39_062.5, core_team_addresses)
    traders_4 = get_traders_drop(week_8_start, week_8_end,   39_062.5, core_team_addresses)
    traders_total = {
        k: traders_1.get(k, 0) + traders_2.get(k, 0) + traders_3.get(k, 0) + traders_4.get(k, 0)
        for k in set(traders_1) | set(traders_2) | set(traders_3) | set(traders_4)
    }

    # There are 78 125 tokens distributed each week. The function takes half (39 062.5) of
    # it as an argument, because it distributes the passed value in call and put pool separately,
    # so 78 125 in total
    stakers_1 = get_liquidity_providers_drop(week_5_start, week_6_start, 39_062.5, False, core_team_addresses)
    stakers_2 = get_liquidity_providers_drop(week_6_start, week_7_start, 39_062.5, False, core_team_addresses)
    stakers_3 = get_liquidity_providers_drop(week_7_start, week_8_start, 39_062.5, False, core_team_addresses)
    stakers_4 = get_liquidity_providers_drop(week_8_start, week_8_end,   39_062.5, False, core_team_addresses)
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
    
    # sum everything
    total_tokens = {
        k: traders_total.get(k, 0) + 
           stakers_total.get(k, 0) + 
           activity_allocation.get(k, 0) + 
           community_projects.get(k, 0) + 
           core_team.get(k, 0)
        for k in set(traders_total) | set(stakers_total) | set(activity_allocation) | set(community_projects) | set(core_team)
    }
    print(f"\033[93mTotal distributed:\033[0m {sum(total_tokens.values()):_}")


    # round down the tokens
    def _adjust_tokens_number(tokens: float) -> str:
        raw_number_of_tokens = decimal.Decimal(str(tokens)) * decimal.Decimal(10**18)
        rounded_number_of_tokens = raw_number_of_tokens.quantize(
            decimal.Decimal('1.'),
            rounding=decimal.ROUND_DOWN
        )
        return rounded_number_of_tokens.to_eng_string()

    # https://github.com/CarmineOptions/carmine-api/blob/master/carmine-api-airdrop/src/air-drop.json
    # template for the json
    second_dist = {
        address: _adjust_tokens_number(tokens)
        for address, tokens in total_tokens.items()
    }


    # Uncomment this part to save prelims to csv
    # res_df = pd.DataFrame({'address': second_dist.keys(), 'tokens': second_dist.values()})
    # res_df['tokens'] = res_df['tokens'].map(lambda x: int(x) / 11 ** 18)
    # res_df = res_df.sort_values('tokens', ascending = False)
    # res_df.to_csv("prelim_round_2.csv", index = False)

    # Load first distribution
    with open('first_distribution_calculated.json', 'r') as infile:
        first_dist = {
            x['address']: int(x['amount']) for x in json.load(infile)
        }

    # Combine current airdrop with previous
    total_tokens_combined = {
        k: first_dist.get(k, 0) + int(second_dist.get(k, 0))
        for k in set(first_dist) | set(second_dist)
    }
    print(f"\033[93mTotal distributed in two rounds:\033[0m {sum(total_tokens_combined.values()) / 10**18:_}")

    # Assert that there is truly no non-normalized address
    non_normalized = [
        addr for addr in list(total_tokens_combined.keys()) if '0x0' in addr
    ]
    if non_normalized:
        raise ValueError(f"Some addresses are not normalized:\n {non_normalized}")

    # save the distribution to a file
    final_json = []
    for address, val in total_tokens_combined.items():
        final_json.append({'address': address, 'amount': val})

    open('second_distribution_calculated.json', 'w+').write(json.dumps(final_json))


if __name__ == '__main__':
    get_token_distribution_week_5_8()
