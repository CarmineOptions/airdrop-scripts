import decimal
import json
from typing import Dict, Any

import pandas as pd

allocation_csv_path = 'src/allocation_7_8_24/Final allocations- season 1.csv'

ROUND = '7-8-24'

def normalize_sn_address(address: str) -> str:
    return hex(int(address, 0))


def normalize_addresses_in_map(address_map: Dict[str, Any]) -> Dict[str, Any]:
    normalized_address_map = {normalize_sn_address(address): tokens for address, tokens in address_map.items()}
    assert len(normalized_address_map) == len(address_map), "Duplicated addresses"
    return normalized_address_map


def get_token_distribution_round_7_8_24() -> Dict[str, int]:
    contributors_df = pd.read_csv(allocation_csv_path, sep=';')
    # Group by 'Starknet address' and sum 'Allocation'
    contributors_df['Starknet address'] = contributors_df['Starknet address'].apply(normalize_sn_address)
    grouped = contributors_df.groupby('Starknet address')['Allocation'].sum().reset_index()
    all_contributors = dict(zip(grouped['Starknet address'], grouped['Allocation']))
    all_contributors_norm = normalize_addresses_in_map(all_contributors)

    all_contributor_maps = [
        all_contributors_norm
    ]
    all_contributor_addresses = {address for contributors in all_contributor_maps for address in contributors}
    # Sum everything
    total_tokens = {
        k: sum([
            contributors_map.get(k, 0) for contributors_map in all_contributor_maps
        ])
        for k in all_contributor_addresses
    }
    print(f"\033[93mTotal distributed in {ROUND}-th round:\033[0m {sum(total_tokens.values()):_}")

    df = pd.DataFrame(index=list(all_contributor_addresses))

    # Add each contributor map as a column in the DataFrame
    column_names = [
        "contributors"
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

    new_dist = {
        address: _adjust_tokens_number(tokens)
        for address, tokens in total_tokens.items()
    }

    # exclude faulty addresses
    faulty_addresses = []
    for address in faulty_addresses:
        del new_dist[address]

    # Uncomment this part to save prelims to csv
    res_df = pd.DataFrame({'address': new_dist.keys(), 'tokens': new_dist.values()})
    res_df['tokens'] = res_df['tokens'].map(lambda x: int(x) / 10 ** 18)
    res_df = res_df.sort_values('tokens', ascending=False)
    res_df.to_csv(f"prelim_round_{ROUND}.csv", index=False)

    # Load previous distribution
    with open('fifth_distribution_calculated.json', 'r') as infile:
        fifth_dist = {
            x['address']: x['amount'] for x in json.load(infile)
        }
    # Combine current airdrop with previous
    total_tokens_combined = {
        k: int(new_dist.get(k, 0)) + int(fifth_dist.get(k, 0))
        for k in set(new_dist) | set(fifth_dist)
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
    open('7-8-24_distribution_calculated.json', 'w+').write(json.dumps(final_json))


if __name__ == '__main__':
    get_token_distribution_round_7_8_24()
