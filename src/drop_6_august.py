import decimal
import json
from typing import Dict, Any

import pandas as pd


ROUND = 6

TOTAL_DISTRIBUTION_FOR_TRADING = 367_676
TOTAL_DISTRIBUTION_FOR_LIQUIDITY_PROVIDERS = 209_460
# VOTING_AND_REFERRAL_TOKENS_PER_POINT = 0.3  # TODO fix

USER_POINTS_FILE_PATH = 'src/allocation_6_docs/user_pounts.csv'


def normalize_sn_address(address: str) -> str:
    return hex(int(address, 0))


def normalize_addresses_in_map(address_map: Dict[str, Any]) -> Dict[str, Any]:
    normalized_address_map = {normalize_sn_address(address): tokens for address, tokens in address_map.items()}
    assert len(normalized_address_map) == len(address_map), "Duplicated addresses"
    return normalized_address_map


def get_token_distribution_round_6() -> Dict[str, int]:
    # user points
    user_points = pd.read_csv(USER_POINTS_FILE_PATH)
    user_points.user_address = user_points.user_address.apply(lambda x: normalize_sn_address(x))

    user_points['user_points_referral_and_voting'] = user_points.apply(lambda x: (
            # x.trading_points * TRADING_MULTIPLIER + x.liquidity_points * LIQUIDITY_MULTIPLIER
            x.referral_points + x.vote_points
    ), axis=1)

    user_points_liquidity_providers_total = user_points.liquidity_points.sum()
    tokens_per_point_liquidity_providers = TOTAL_DISTRIBUTION_FOR_LIQUIDITY_PROVIDERS/user_points_liquidity_providers_total

    user_points_traders_total = user_points.trading_points.sum()
    tokens_per_point_traders = TOTAL_DISTRIBUTION_FOR_TRADING / user_points_traders_total

    print(f"Tokens for user points: \n   Liquidity porviders: {tokens_per_point_liquidity_providers} \n"
          f"   Traders: {tokens_per_point_traders}")

    assert len(user_points.user_address.unique()) == user_points.shape[0], "Addresses for timestamp are not unique"

    user_points_trading_norm = {
        row.user_address: row.trading_points * tokens_per_point_traders
        for _, row in user_points.iterrows()
    }
    user_points_liquidity_providers_norm = {
        row.user_address: row.liquidity_points * tokens_per_point_liquidity_providers
        for _, row in user_points.iterrows()
    }
    user_points_referral_and_voting_norm = {
        row.user_address: row.user_points_referral_and_voting * tokens_per_point_traders
        for _, row in user_points.iterrows()
    }


    community = {
        "0x018D4756921D34b0026731F427C6b365687Ce61CE060141Bf26867f0920D2191": 6000,
        "0x01fb62ac54f9fa99e1417f83bcb88485556427397f717ed4e7233bc99be31bff": 6000,
        "0x054e0ab67bd384312d640915b55d7e918fe2031269ec26f8fc7fde9abbd1e0a5": 10000,
        "0x00a975351cf03ad81d5d08f953dcc415da07012ff6d2d44a074c384feb0db35d": 8000,
        "0x039e14d815587cdd5ae400684e5d60848d9a134b378260cc1f2de6e7aedcdb45": 8000,
        "0x04a8713ab7aff5e97fb1aa7652314a5ed6102b200da75ef42078a5a01fef4093": 4000,
        "0x00aa7fe49a402af47bf2bcfee7e356a5ae18db0adedaa2c44a1de60c6ef9caef": 4000,
        "0x0558808A3C00c778C93E3d4348687b048613993E6b03836726B5d581f9960515": 4000,
        "0x000928e2956ad7138c273120412bf2283d83e985b2426c2b8ddf146fd6b37884": 4000,
        "0x02ba1c396a2a3bd5dcc62fe3f9bd9f85eaa6580609bb903ccbb8aad374cf3f76": 4000,
        "0x05bb61ab3472556d0151bb4fa22e3514d1a490cb31229b7bcca33744afd5858f": 4000,
        "0x046d95a7f86ec19412a4da5d28f6a6addf62f1cd2c5d0defbe18bff1d96a2458": 4000,
        "0x049c691d23cf572e3318472dac01d5a6d996470aa1050af0ccadda392c073efb": 4000,
        "0x06Ae3E526C67A3f38393034abAC34E8274A5683c2c4f00D6aeFEa98057daE5Af": 4000,
        "0x055f973e925Fba11C9cEA1565ff000f196a7DdfCb73c7292774a8d5408FA6bF4": 4000,
        "0x0639F7aD800Fcbe2aD56E3b000f9A0581759CcE989b3Ee09477055c0816A12c7": 2000,
    }

    community_norm = normalize_addresses_in_map(community)
    print(f"Total tokens for COMMUNITY: {sum(community_norm.values())}")

    all_contributor_maps = [
        user_points_trading_norm,
        user_points_liquidity_providers_norm,
        user_points_referral_and_voting_norm,
        community_norm
    ]
    all_contributor_addresses = {address for contributors in all_contributor_maps for address in contributors}
    # Sum everything
    total_tokens = {
        k: sum([
            contributors_map.get(k, 0) for contributors_map in all_contributor_maps
        ])
        for k in all_contributor_addresses
    }
    print(f"\033[93mTotal distributed in {ROUND}th round:\033[0m {sum(total_tokens.values()):_}")

    #
    df = pd.DataFrame(index=list(all_contributor_addresses))

    # Add each contributor map as a column in the DataFrame
    column_names = [
        "user_points_trading_norm",
        "user_points_liquidity_providers_norm",
        "user_points_referral_and_voting_norm",
        "community_norm"
    ]

    for column_name, contributors_map in zip(column_names, all_contributor_maps):
        df[column_name] = df.index.map(contributors_map).fillna(0)

    # Calculate the total points for each contributor
    df['total'] = df.sum(axis=1)
    df.to_csv(f"round_{ROUND}_per_cat.csv")

    # Round down the tokens
    def _adjust_tokens_number(tokens: float) -> str:
        raw_number_of_tokens = decimal.Decimal(str(tokens)) * decimal.Decimal(10 ** 18)
        rounded_number_of_tokens = raw_number_of_tokens.quantize(
            decimal.Decimal('1.'),
            rounding=decimal.ROUND_DOWN
        )
        return rounded_number_of_tokens.to_eng_string()

    sixth_dist = {
        address: _adjust_tokens_number(tokens)
        for address, tokens in total_tokens.items()
    }

    # exclude faulty addresses
    faulty_addresses = []
    for address in faulty_addresses:
        del sixth_dist[address]

    # Uncomment this part to save prelims to csv
    res_df = pd.DataFrame({'address': sixth_dist.keys(), 'tokens': sixth_dist.values()})
    res_df['tokens'] = res_df['tokens'].map(lambda x: int(x) / 10 ** 18)
    res_df = res_df.sort_values('tokens', ascending = False)
    res_df.to_csv(f"prelim_round_{ROUND}.csv", index = False)

    # Load PREVIOUS distribution
    with open('7-8-24_distribution_calculated.json', 'r') as infile:
        last_dist = {
            x['address']: x['amount'] for x in json.load(infile)
        }
    # Combine current airdrop with previous
    total_tokens_combined = {
        k: int(last_dist.get(k, 0)) + int(sixth_dist.get(k, 0))
        for k in set(last_dist) | set(sixth_dist)
    }
    print(f"\033[93mTotal distributed in {ROUND} rounds:\033[0m {sum(total_tokens_combined.values()) / 10**18:_}")

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
    open(f'{ROUND}th_distribution_calculated.json', 'w+').write(json.dumps(final_json))


if __name__ == '__main__':
    get_token_distribution_round_6()
