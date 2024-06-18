from typing import Dict, Any
import os
import re

import pandas as pd


REFERRAL_MULTIPLIER = 1
VOTE_MULTIPLIER = 1
LIQUIDITY_MULTIPLIER = 1
TRADING_MULTIPLIER = 1

USER_POINTS_FILE_PATH = '../user_POINTS.csv'
OG_USERS_FILE_PATH = '../og-users.txt'
TESTNET_USERS_FILE_PATH = '../testnet-users.txt'


def extract_starknet_addresses(file_path):
    # Define the regex pattern for StarkNet addresses with variable length after 0x
    address_pattern = r'0x[a-fA-F0-9]{48,64}'

    # Read the content of the file
    with open(file_path, 'r') as file:
        content = file.read()

    # Find all addresses matching the pattern
    addresses = re.findall(address_pattern, content)

    return addresses


def normalize_sn_address(address: str) -> str:
    return hex(int(address, 0))


def normalize_addresses_in_map(address_map: Dict[str, Any]) -> Dict[str, Any]:
    normalized_address_map = {normalize_sn_address(address): tokens for address, tokens in address_map.items()}
    assert len(normalized_address_map) == len(address_map), "Duplicated addresses"
    return normalized_address_map


def get_token_distribution_round_4() -> Dict[str, int]:
    distribution_model = {
        "Specific users": 20_000,
        "Lead Ambassadors": None,
        "Ambassadors1": 500_000,
        "Ambassadors2": None,
        "Carmine watch (Moderators)": 200_000,
        "Community devs (DeRisk)": 200_000,
        "Community devs (Konoha)": 200_000,
        "OG discord users": 3350,
        "testnet users": 9420,
        "KOLs": 200_000,
        "zealy users": 100_000,
        "Galxe user": 100_000,
        "Gitcoin contributors": 200_000,
        "Galxe flippening": 20_000
    }

    # Lead ambassadors, ambassadors, moderators
    ambassadors= {
        "f": distribution_model['Ambassadors1'],
        "c": distribution_model['Ambassadors2'],
        "moderator": distribution_model[]
    }
    ambassadors_norm = normalize_addresses_in_map(ambassadors)

    moderator_addresses = []  # TODO add addresses
    moderator_addresses = {normalize_sn_address(address) for address in moderator_addresses}
    total_tokens_allocated_mods = distribution_model["Carmine watch (Moderators)"]
    allocation_per_mod = total_tokens_allocated_mods / len(moderator_addresses)
    moderators_norm = {address: allocation_per_mod for address in moderator_addresses}

    # investors
    investors = {
        '0x05a4523982b437aadd1b5109b6618c46f7b1c42f5f9e7de1a3b84091f87d411b': None,
        # TODO add 3 more, add number above
    }
    investors_norm = normalize_addresses_in_map(investors)

    KOL = {}
    zealy_users = {}
    galxe_users = {}
    gitcoin_contributors = {}
    poolcleaners = {}


    # Core Team
    core_team = {
        "0x00d79a15d84f5820310db21f953a0fae92c95e25d93cb983cc0c27fc4c52273c": 7001443
        # TODO add all
    }
    core_team_norm = normalize_addresses_in_map(core_team)

    # user points
    user_points = pd.read_csv(USER_POINTS_FILE_PATH)
    user_points['user_points_total'] = user_points.apply(lambda x: (
            x.trading_points * TRADING_MULTIPLIER + x.liquidity_points * LIQUIDITY_MULTIPLIER
            + x.referral_points * REFERRAL_MULTIPLIER + x.vote_points * VOTE_MULTIPLIER
    ), axis=1)
    user_points.user_address = user_points.user_address.apply(lambda x: normalize_sn_address(x))

    assert len(user_points.user_address.unique()) == user_points.shape[0], "Addresses for timestamp are not unique"
    user_points_norm = {row.user_address: row.user_points_total for _, row in user_points.iterrows()}

    # f.s.users
    fsusers = {
        '0x00a975351cf03ad81d5d08f953dcc415da07012ff6d2d44a074c384feb0db35d': 7500,
        '0x039e14d815587cdd5ae400684e5d60848d9a134b378260cc1f2de6e7aedcdb45': 12500
    }
    fsusers_norm = normalize_addresses_in_map(fsusers)

    # contributors:
    # DeRisk
    derisk_contributor_days = {
        '0x04418e71dfea541134c45c3af1f06c7e053838179a9d072b5f1b79a855561e28': 0.25,
        '0x058f91a1f81fe126466a4d5e75450409d552d5433ba53c75858a750acaab864f': 1,
        '0x0388012BD4385aDf3b7afDE89774249D5179841cBaB06e9E5b4045F27B327CE8': 1.5,
        '0x004fde84a79f786872566557601cb23B53620546ab74999d0794D9E00751f083': 2.5,
        '0x0582d5Bc3CcfCeF2F7aF1FdA976767B010E453fF487A7FD2ccf9df1524f4D8fC': 14,
        '0x020281104e6cb5884dabcdf3be376cf4ff7b680741a7bb20e5e07c26cd4870af': 35,
        '0x066d2f353fc19409cb19ae6af94c1ce6fb8d6a6a39cb46586ce422b1deef3758': 0.5,
        '0x06c7f6FD1f83d144991bdD52c8b6e9Fe00995Da18BB856C755a259f30Eb04337': 16,
        '0x035e0e8eb2c70d17beae02a3f6be24c78457dbf81833e16b225c19ca23849bcf': 2.25,
        '0x03bc748ed0d769dc477c1f8b199ed0d97f9f86709af6adc8779e9e05a6e47f03': 0.5,
        '0x069DE8104EB7abeBb3f93c8245ef83545336feD4055FE45F55C2cDDB9931C5f1': 7,
        '0x04cced5156ab726bf0e0ca2afeb1f521de0362e748b8bdf07857b088dbc7b457': 3
    }
    total_days = sum(derisk_contributor_days.values())

    total_tokens_allocated = distribution_model["Community devs (DeRisk)"]
    allocation_per_day = total_tokens_allocated / total_days
    derisk_contributors = {address: allocation_per_day * days for address, days in derisk_contributor_days.items()}
    derisk_contributors_norm = normalize_addresses_in_map(derisk_contributors)

    # Konoha
    konoha_contributor_days = {
        '0x01f0d3e6e3b1116fbf69dd670e5c079c8c3b6e5a789f00270ba049b6c22a0d3b': 3,
        '0x07e2d149567391f4269842a3e01be088ac0dca25594583f85b43b5090234449c': 4,
        '0x007b275f7524f39b99a51c7134bc44204fedc5dd1e982e920eb2047c6c2a71f0': 1,
        '0x01717612798ef3802ba6efed6f04ed2ba0a624f1dcb8879fd44cd93d7f54484b': 7,
        '0x053a629c98a1ef74b0961b765b2b4bf50ce5a9725be3e14a7fa95bcc61f872db': 5,
        '0x0486deba6028c880ce3d1730a4496e4f12d7b813367d43510ea410f5ff7e3efb': 30,
        '0x00a33c61ad75096f4c67449f561cf4d84ef00c318f4c6e163926987cd5befddc': 6,
        '0x075e108742924A335b3F4589ea74aC0C6fF89B61E05Bd72Cb244CEcCeEF42550': 4,
    }

    total_days = sum(konoha_contributor_days.values())

    total_tokens_allocated = distribution_model["Community devs (Konoha)"]
    allocation_per_day = total_tokens_allocated / total_days
    konoha_contributors = {address: allocation_per_day * days for address, days in konoha_contributor_days.items()}
    konoha_contributors_norm = normalize_addresses_in_map(konoha_contributors)

    # testnet_contributors
    testnet_addresses = extract_starknet_addresses(TESTNET_USERS_FILE_PATH)
    testnet_addresses = {normalize_sn_address(address) for address in testnet_addresses}
    token_per_testnet_contributor = distribution_model["testnet users"] / len(testnet_addresses)
    testnet_contributors_norm = {
        address: token_per_testnet_contributor for address in testnet_addresses
    }

    # OG contributors
    og_user_addresses = extract_starknet_addresses(OG_USERS_FILE_PATH)
    og_user_addresses = {normalize_sn_address(address) for address in og_user_addresses}
    token_per_og_contributor = distribution_model["OG discord users"] / len(og_user_addresses)
    og_contributors_norm = {
        address: token_per_og_contributor for address in og_user_addresses
    }


    # # Normalize the addresses before summing up so that no values are lost
    # traders_total       = {hex(int(key, 0)): value for key, value in traders_total.items()}
    # stakers_total       = {hex(int(key, 0)): value for key, value in stakers_total.items()}
    # community_projects  = {hex(int(key, 0)): value for key, value in community_projects.items()}
    # activity_allocation = {hex(int(key, 0)): value for key, value in activity_allocation.items()}
    # core_team           = {hex(int(key, 0)): value for key, value in core_team.items()}
    #
    # Sum everything
    total_tokens = {
        k: traders_total.get(k, 0) +
           stakers_total.get(k, 0) +
           activity_allocation.get(k, 0) +
           community_projects.get(k, 0) +
           core_team.get(k, 0)
        for k in set(traders_total) | set(stakers_total) | set(activity_allocation) | set(community_projects) | set(core_team)
    }
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
