import decimal
import json
from typing import Dict, Any

import pandas as pd


ROUND = 8

TOTAL_DISTRIBUTION_FOR_TRADING = 367_676
TOTAL_DISTRIBUTION_FOR_LIQUIDITY_PROVIDERS = 209_460

USER_POINTS_FILE_PATH = 'src/allocation_eight/user-points.csv'


def normalize_sn_address(address: str) -> str:
    return hex(int(address, 0))


def normalize_addresses_in_map(address_map: Dict[str, Any]) -> Dict[str, Any]:
    normalized_address_map = {normalize_sn_address(address): tokens for address, tokens in address_map.items()}
    assert len(normalized_address_map) == len(address_map), "Duplicated addresses"
    return normalized_address_map


def get_token_distribution_round_8() -> None:
    # user points
    user_points = pd.read_csv(USER_POINTS_FILE_PATH)
    user_points.user_address = user_points.user_address.apply(lambda x: normalize_sn_address(x))

    user_points['user_points_referral_and_voting'] = user_points.apply(lambda x: (
            x.referral_points + x.vote_points
    ), axis=1)

    user_points_liquidity_providers_total = user_points.liquidity_points.sum()
    tokens_per_point_liquidity_providers = TOTAL_DISTRIBUTION_FOR_LIQUIDITY_PROVIDERS/user_points_liquidity_providers_total

    user_points_traders_total = user_points.trading_points.sum()
    tokens_per_point_traders = TOTAL_DISTRIBUTION_FOR_TRADING / user_points_traders_total

    print(f"Tokens for user points: \n   Liquidity porviders: {tokens_per_point_liquidity_providers} \n"
          f"   Traders / Refferal / Voting: {tokens_per_point_traders}")

    assert len(user_points.user_address.unique()) == user_points.shape[0], "Addresses for timestamp are not unique"

    user_points_trading_norm = {
        row.user_address: row.trading_points * tokens_per_point_traders
        for _, row in user_points.iterrows()
    }
    print(f"Total tokens for trading: {sum(user_points_trading_norm.values())}")
    user_points_liquidity_providers_norm = {
        row.user_address: row.liquidity_points * tokens_per_point_liquidity_providers
        for _, row in user_points.iterrows()
    }
    print(f"Total tokens for providing liquidity: {sum(user_points_liquidity_providers_norm.values())}")
    user_points_referral_and_voting_norm = {
        row.user_address: row.user_points_referral_and_voting * tokens_per_point_traders
        for _, row in user_points.iterrows()
    }
    print(f"Total tokens for referral and voting: {sum(user_points_referral_and_voting_norm.values())}")

    community = {
        '0x018D4756921D34b0026731F427C6b365687Ce61CE060141Bf26867f0920D2191': 2000,
        '0x054e0ab67bd384312d640915b55d7e918fe2031269ec26f8fc7fde9abbd1e0a5': 2300,
        '0x039e14d815587cdd5ae400684e5d60848d9a134b378260cc1f2de6e7aedcdb45': 2000,
        '0x0558808A3C00c778C93E3d4348687b048613993E6b03836726B5d581f9960515': 1500,
        '0x00a975351cf03ad81d5d08f953dcc415da07012ff6d2d44a074c384feb0db35d': 1500,
        '0x02ba1c396a2a3bd5dcc62fe3f9bd9f85eaa6580609bb903ccbb8aad374cf3f76': 2500,
        '0x050c439fCfA077cd4a1ff4477C5242D4781010D9B1C0f1e2a96980896eD63A38': 2200,
        '0x05bb61ab3472556d0151bb4fa22e3514d1a490cb31229b7bcca33744afd5858f': 1500,
        '0x06496c659adab5aeeb34d7767f697ad41abfec046584313fe54fc304804fb195': 2000,
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

    #################### adjust allocation for selected users: ####################e
    sel_users = [
        0x029c339266a9ad35d5Cc64c23bf13b7156e72c27B7dF743661537A98Af8260b3,
        0x01f756725531f4d85790382430ef13a0d9acc0eb149f443febc1bcdc1ea7ce2e,
        0x001d2866c8604932058868F0865095BEce599ec576C5Cc0F2CA8B4714Df7128A,
        0x00a975351cf03ad81d5d08f953dcc415da07012ff6d2d44a074c384feb0db35d,
        0x0449E8CdA692fC1F791F721B36Aa4d636393e160C9B561396F07787f82D02815,
        0x02D86897DaaDeE2DFFDB5C5B734aB568fE849808105977e0384F8E5D1a0d33D7,
        0x0718505b87b5a448205ae22ac84a21b9e568b532ed95285c4c03973f8b1a73e8,
        0x067Aa1C8B9dBaf98d8A83D57b31185c9c29868d329c3bF9Ee3a0d6820f95D4a1,
        0x01dc8f0c2077757132d16daabc9f9e23336872ac351fd75979f0362dccd1bd49
    ]
    sel_user_hexes = [hex(u) for u in sel_users]
    for allocation_map in  [
        user_points_trading_norm,
        user_points_liquidity_providers_norm,
        user_points_referral_and_voting_norm
    ]:
        for sel_user in sel_user_hexes:
            allocated_amount = allocation_map.get(sel_user, 0)
            if allocated_amount:
                allocation_map[sel_user] = allocated_amount * 1.1
        # Sum everything
    total_tokens_0 = {
        k: sum([
            contributors_map.get(k, 0) for contributors_map in all_contributor_maps
        ])
        for k in all_contributor_addresses
    }
    print(f"\033[93mExtra tokens distributed:\033[0m {sum(total_tokens_0.values()) - sum(total_tokens.values()):_}")
    ###########################################################################################

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
    with open(f'{ROUND - 1}th_distribution_calculated.json', 'r') as infile:
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
        {'address': address, 'amount': str(val)}
        for address, val in total_tokens_combined.items()
    ]
    open(f'{ROUND}th_distribution_calculated.json', 'w+').write(json.dumps(final_json))


if __name__ == '__main__':
    get_token_distribution_round_8()
