import decimal
import json
from typing import Dict, Any

import pandas as pd


REFERRAL_MULTIPLIER = 1
VOTE_MULTIPLIER = 1
LIQUIDITY_MULTIPLIER = 1
TRADING_MULTIPLIER = 1
TOKEN_PER_POINT = 0.3

USER_POINTS_FILE_PATH = 'src/allocation_four_docs/user-POINTS-2024-07-18.csv'


def normalize_sn_address(address: str) -> str:
    return hex(int(address, 0))


def normalize_addresses_in_map(address_map: Dict[str, Any]) -> Dict[str, Any]:
    normalized_address_map = {normalize_sn_address(address): tokens for address, tokens in address_map.items()}
    assert len(normalized_address_map) == len(address_map), "Duplicated addresses"
    return normalized_address_map


def get_token_distribution_round_5() -> Dict[str, int]:
    # user points
    user_points = pd.read_csv(USER_POINTS_FILE_PATH)
    user_points['user_points_total'] = user_points.apply(lambda x: (
            x.trading_points * TRADING_MULTIPLIER + x.liquidity_points * LIQUIDITY_MULTIPLIER
            + x.referral_points * REFERRAL_MULTIPLIER + x.vote_points * VOTE_MULTIPLIER
    ), axis=1)
    user_points.user_address = user_points.user_address.apply(lambda x: normalize_sn_address(x))
    tokens_per_point = TOKEN_PER_POINT
    user_points['user_tokens'] = user_points.user_points_total * tokens_per_point
    print(f"Tokens for user points: {user_points['user_tokens'].sum()}")

    assert len(user_points.user_address.unique()) == user_points.shape[0], "Addresses for timestamp are not unique"
    user_points_norm = {row.user_address: row.user_tokens for _, row in user_points.iterrows()}

    marketing_norm = {normalize_sn_address(''): 0}  # TODO add address and amount

    cl_norm = {normalize_sn_address(''): 0}  # TODO add address and amount

    all_contributor_maps = [
        user_points_norm,
        marketing_norm,
        cl_norm
    ]
    all_contributor_addresses = {address for contributors in all_contributor_maps for address in contributors}
    # Sum everything
    total_tokens = {
        k: sum([
            contributors_map.get(k, 0) for contributors_map in all_contributor_maps
        ])
        for k in all_contributor_addresses
    }
    print(f"\033[93mTotal distributed in 4th round:\033[0m {sum(total_tokens.values()):_}")

    #
    df = pd.DataFrame(index=list(all_contributor_addresses))

    # Add each contributor map as a column in the DataFrame
    column_names = [
        "core_team", "ambassadors", "moderators", 'ambassadors_f_norm',
        'investors_norm',
        'user_points_norm',
        'konoha_contributors_norm',
        'derisk_contributors_norm',
        'og_contributors_norm',
        'testnet_contributors_norm',
        'fsusers_norm',
        'KOL_norm'
    ]

    for column_name, contributors_map in zip(column_names, all_contributor_maps):
        df[column_name] = df.index.map(contributors_map).fillna(0)

    # Calculate the total points for each contributor
    df['total'] = df.sum(axis=1)
    df.to_csv("round_4_per_cat.csv")

    # Round down the tokens
    def _adjust_tokens_number(tokens: float) -> str:
        raw_number_of_tokens = decimal.Decimal(str(tokens)) * decimal.Decimal(10 ** 18)
        rounded_number_of_tokens = raw_number_of_tokens.quantize(
            decimal.Decimal('1.'),
            rounding=decimal.ROUND_DOWN
        )
        return rounded_number_of_tokens.to_eng_string()

    fifth_dist = {
        address: _adjust_tokens_number(tokens)
        for address, tokens in total_tokens.items()
    }

    # exclude faulty addresses
    faulty_addresses = []
    for address in faulty_addresses:
        del fifth_dist[address]

    # Uncomment this part to save prelims to csv
    res_df = pd.DataFrame({'address': fifth_dist.keys(), 'tokens': fifth_dist.values()})
    res_df['tokens'] = res_df['tokens'].map(lambda x: int(x) / 10 ** 18)
    res_df = res_df.sort_values('tokens', ascending = False)
    res_df.to_csv("prelim_round_5.csv", index = False)

    # Load second distribution
    with open('fourth_distribution_calculated.json', 'r') as infile:
        fourth_dist = {
            x['address']: x['amount'] for x in json.load(infile)
        }
    # Combine current airdrop with previous
    total_tokens_combined = {
        k: int(fourth_dist.get(k, 0)) + int(fifth_dist.get(k, 0))
        for k in set(fourth_dist) | set(fifth_dist)
    }
    print(f"\033[93mTotal distributed in four rounds:\033[0m {sum(total_tokens_combined.values()) / 10**18:_}")

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
    open('fifth_distribution_calculated.json', 'w+').write(json.dumps(final_json))


if __name__ == '__main__':
    get_token_distribution_round_5()
