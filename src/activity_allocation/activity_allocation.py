# As per https://medium.com/@carminefinanceinfo/inside-carmine-options-amm-a-complete-breakdown-of-token-distribution-and-allocation-21a7f75e9bca
# and specifically 
#
# First month the split will be based on collected “points”. Users will receive a percentage from the 400k Carmine tokens based on the “User’s points divided by all points”. Points will be collected only if user uses mainnet and will be collected for:
# +1 for mainnet trading — conditions are hidden to decrease sybil farming
# +0.5 for both trading and staking on mainnet (assumes single wallet address) — conditions are hidden to decrease sybil farming
# +1.2 for having testnet role (addresses will be collected over discord soon)
# +2 for having OG role (addresses will be collected over discord soon)
# +1 for having quiz role (addresses will be collected over discord soon)

# We also manually took care of multiaccounts (sybil attacks). Sadly to were not able to do this accross all sections, just few :/

from typing import Dict, List


TOKEN_ALLOCATION = 400_000


def get_activity_allocation(
    trading_activity_addresses: List[str],
    staking_activity_addresses: List[str],
    processed_OGs_filename: str,
    processed_testnet_filename: str,
    period: str
) -> Dict[str, float]:
    # This works only for the first four weeks
    if period != 'week_1_4':
        raise ValueError

    # standardize the addresses
    trading_activity_addresses = [hex(int(x, 0)) for x in trading_activity_addresses]
    staking_activity_addresses = [hex(int(x, 0)) for x in staking_activity_addresses]

    activity_points = {} # Dict[address, points]

    trading_points = {address: 1 for address in trading_activity_addresses}
    staking_points = {address: 1 for address in staking_activity_addresses}
    mainnet_acitivity_points = trading_points | staking_points

    both_trade_stake = {address: 0.5 for address in set(trading_activity_addresses) & set(staking_activity_addresses)}
    
    # For comparison purposses the addresses are unified
    OGs = {hex(int(x, 0)): 2  for x in (open(processed_OGs_filename, 'r').read().split('\n')) if x != ''}
    testers = {hex(int(x, 0)): 1.2 for x in (open(processed_testnet_filename, 'r').read().split('\n')) if x != ''}
    # quiz winners got OG roles... that was a bug in the article

    total_points = {}
    for address, mainnet_acitivity_point in mainnet_acitivity_points.items():
        total_points[address] = mainnet_acitivity_point
        total_points[address] += both_trade_stake.get(address, 0)
        total_points[address] += OGs.get(address, 0)
        total_points[address] += testers.get(address, 0)

    sum_of_points = sum(point for point in total_points.values())

    total_tokens = {address: points * TOKEN_ALLOCATION / sum_of_points for address, points in total_points.items()}
    return total_tokens
