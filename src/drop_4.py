from typing import Dict
import os

import pandas as pd



REFERRAL_MULTIPLIER = 1
VOTE_MULTIPLIER = 1
LIQUIDITY_MULTIPLIER = 1
TRADING_MULTIPLIER = 1

USER_POINTS_FILE_PATH = '../user_POINTS.csv'
OG_USERS_FILE_PATH = '../og-users.txt'
TESTNET_USERS_FILE_PATH = '../testnet-users.txt'


def get_token_distribution_round_4() -> Dict[str, int]:
    distribution_model = {
        "Specific users": 20_000,
        "Lead Ambassadors": None,
        "Ambassadors1": 500_000,
        "Ambassadors2": None,
        "Carmine watch (Moderators)": 200_000,
        "Community devs (DeRisk)": 200_000,
        "Community devs (Konoha)": 200_000,
        "OG discord users": 50,
        "testnet users": 20,
        "KOLs": 200_000,
        "zealy users": 100_000,
        "Galxe user": 100_000,
        "Gitcoin contributors": 200_000,
        "Galxe flippening": 20_000
    }
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
    }

    core_team_addresses = {
    }

    # user points
    user_points = pd.read_csv(USER_POINTS_FILE_PATH)
    user_points['user_points_total'] = user_points.apply(lambda x: (
            x.trading_points * TRADING_MULTIPLIER + x.liquidity_points * LIQUIDITY_MULTIPLIER
            + x.referral_points * REFERRAL_MULTIPLIER + x.vote_points * VOTE_MULTIPLIER
    ), axis=1)

    assert len(user_points.user_address.unique()) == user_points.shape[0], "Addresses for timestamp are not unique"
    user_points_dict = {row.user_address: row.user_points_total for _, row in user_points.iterrows()}

    # contributors:



    # # Normalize the addresses before summing up so that no values are lost
    # traders_total       = {hex(int(key, 0)): value for key, value in traders_total.items()}
    # stakers_total       = {hex(int(key, 0)): value for key, value in stakers_total.items()}
    # community_projects  = {hex(int(key, 0)): value for key, value in community_projects.items()}
    # activity_allocation = {hex(int(key, 0)): value for key, value in activity_allocation.items()}
    # core_team           = {hex(int(key, 0)): value for key, value in core_team.items()}
    #
    # # Sum everything
    # total_tokens = {
    #     k: traders_total.get(k, 0) +
    #        stakers_total.get(k, 0) +
    #        activity_allocation.get(k, 0) +
    #        community_projects.get(k, 0) +
    #        core_team.get(k, 0)
    #     for k in set(traders_total) | set(stakers_total) | set(activity_allocation) | set(community_projects) | set(core_team)
    # }
    # print(f"\033[93mTotal distributed in third round:\033[0m {sum(total_tokens.values()):_}")
    #
    # # Round down the tokens
    # def _adjust_tokens_number(tokens: float) -> str:
    #     raw_number_of_tokens = decimal.Decimal(str(tokens)) * decimal.Decimal(10**18)
    #     rounded_number_of_tokens = raw_number_of_tokens.quantize(
    #         decimal.Decimal('1.'),
    #         rounding=decimal.ROUND_DOWN
    #     )
    #     return rounded_number_of_tokens.to_eng_string()
    #
    #
    # # https://github.com/CarmineOptions/carmine-api/blob/master/carmine-api-airdrop/src/air-drop.json
    # # template for the json
    # third_dist = {
    #     address: _adjust_tokens_number(tokens)
    #     for address, tokens in total_tokens.items()
    # }
    #
    #
    # # Uncomment this part to save prelims to csv
    # res_df = pd.DataFrame({'address': third_dist.keys(), 'tokens': third_dist.values()})
    # res_df['tokens'] = res_df['tokens'].map(lambda x: int(x) / 10 ** 18)
    # res_df = res_df.sort_values('tokens', ascending = False)
    # res_df.to_csv("prelim_round_4.csv", index = False)
    #
    # # Load second distribution
    # with open('second_distribution_calculated.json', 'r') as infile:
    #     fourth_dist = {
    #         x['address']: x['amount'] for x in json.load(infile)
    #     }
    #
    #
    # # Combine current airdrop with previous
    # total_tokens_combined = {
    #     k: int(second_dist.get(k, 0)) + int(third_dist.get(k, 0)) + int(fourth_dist.get(k, 0))
    #     for k in set(second_dist) | set(third_dist) | set(fourth_dist)
    # }
    # print(f"\033[93mTotal distributed in three rounds:\033[0m {sum(total_tokens_combined.values()) / 10**18:_}")
    #
    #
    # # Assert that there is truly no non-normalized address
    # non_normalized = [
    #     addr for addr in list(total_tokens_combined.keys()) if '0x0' in addr
    # ]
    # if non_normalized:
    #     raise ValueError(f"Some addresses are not normalized:\n {non_normalized}")
    #
    #
    # final_json = [
    #     {'address': address, 'amount': val}
    #     for address, val in total_tokens_combined.items()
    # ]
    #
    # open('third_distribution_calculated.json', 'w+').write(json.dumps(final_json))


if __name__ == '__main__':
    get_token_distribution_round_4()
