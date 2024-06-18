import decimal
import json
from typing import Dict, Any
import re

import pandas as pd


REFERRAL_MULTIPLIER = 1
VOTE_MULTIPLIER = 1
LIQUIDITY_MULTIPLIER = 1
TRADING_MULTIPLIER = 1

USER_POINTS_FILE_PATH = 'src/allocation_four_docs/user_POINTS.csv'
OG_USERS_FILE_PATH = 'src/allocation_four_docs/og-users.txt'
TESTNET_USERS_FILE_PATH = 'src/allocation_four_docs/testnet-users.txt'


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
    try:
        return hex(int(address, 0))
    except ValueError:  # TODO remove this
        return address


def normalize_addresses_in_map(address_map: Dict[str, Any]) -> Dict[str, Any]:
    normalized_address_map = {normalize_sn_address(address): tokens for address, tokens in address_map.items()}
    assert len(normalized_address_map) == len(address_map), "Duplicated addresses"
    return normalized_address_map


def get_token_distribution_round_4() -> Dict[str, int]:
    distribution_model = {
        "allocated for points": 8_000_000,
        "Specific users": 20_000,
        "Lead Ambassadors": 0,  # TODO ADD number
        "Ambassadors1": 500_000,
        "Ambassadors2": 0,  # TODO ADD number
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

    # Lead ambassadors, ambassadors, moderators  # TODO lead ambassadors
    ambassadors = {
        "f": distribution_model['Ambassadors1'],
        "c": distribution_model['Ambassadors2'],
    }
    ambassadors_norm = normalize_addresses_in_map(ambassadors)

    moderator_addresses = [
        'mod1'
    ]  # TODO add addresses
    moderator_addresses = {normalize_sn_address(address) for address in moderator_addresses}
    total_tokens_allocated_mods = distribution_model["Carmine watch (Moderators)"]
    allocation_per_mod = total_tokens_allocated_mods / len(moderator_addresses)
    moderators_norm = {address: allocation_per_mod for address in moderator_addresses}

    # investors
    investors = {
        '0x05a4523982b437aadd1b5109b6618c46f7b1c42f5f9e7de1a3b84091f87d411b': 0,  # TODO ADD number
        # TODO add 3 more, add number above
    }
    investors_norm = normalize_addresses_in_map(investors)

    # TODO
    KOL_norm = {}
    zealy_users_norm = {}
    galxe_users_norm = {}
    gitcoin_contributors_norm = {}
    poolcleaners_norm = {}
    SKY_norm = {}


    # Core Team
    core_team = {  # TODO add missing addresses
        '0x00d79a15d84f5820310db21f953a0fae92c95e25d93cb983cc0c27fc4c52273c': 7_001_443,
        'm': 112_360,
        '0x06e2c2a5da2e5478b1103d452486afba8378e91f32a124f0712f09edd3ccd923': 2_774_035,
        'd': 1_818_602,
        '0x062c290f0afa1ea2d6b6d11f6f8ffb8e626f796e13be1cf09b84b2edaa083472': 116_389,
        '0x06717eaf502baac2b6b2c6ee3ac39b34a52e726a73905ed586e757158270a0af': 1_664_844,
        '0x07fce7a88b861dfea6af35d16cd60f4ea3bba98dc7b596d4ca529b6c182fd3fd': 417_600,
        'p': 111_385,
        'g': 128_943,
        '0x05105649f42252f79109356e1c8765b7dcdb9bf4a6a68534e7fc962421c7efd2': 210_101,
        '0x06c59d2244250f2540a2694472e3c31262e887ff02582ef864bf0e76c34e1298': 57_795,
        '0x0528f064c43e2d6Ee73bCbfB725bAa293CD31Ea1f1861EA2F80Bc283Ea4Ad728': 120_614,
        '0x00777558f1c767126461540d1f10118981d30bd620707e99686bfc9f00ae66f0': 4_123
    }
    core_team_norm = normalize_addresses_in_map(core_team)

    # user points
    user_points = pd.read_csv(USER_POINTS_FILE_PATH)
    user_points['user_points_total'] = user_points.apply(lambda x: (
            x.trading_points * TRADING_MULTIPLIER + x.liquidity_points * LIQUIDITY_MULTIPLIER
            + x.referral_points * REFERRAL_MULTIPLIER + x.vote_points * VOTE_MULTIPLIER
    ), axis=1)
    user_points.user_address = user_points.user_address.apply(lambda x: normalize_sn_address(x))
    tokens_per_point = distribution_model["allocated for points"]/user_points.user_points_total.sum()
    user_points['user_tokens'] = user_points.user_points_total * tokens_per_point

    assert len(user_points.user_address.unique()) == user_points.shape[0], "Addresses for timestamp are not unique"
    user_points_norm = {row.user_address: row.user_tokens for _, row in user_points.iterrows()}

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

    all_contributor_maps = [
        core_team_norm,
        ambassadors_norm,
        moderators_norm,
        investors_norm,
        user_points_norm,
        konoha_contributors_norm,
        derisk_contributors_norm,
        og_contributors_norm,
        testnet_contributors_norm,
        fsusers_norm,
        # TODO check if following maps are filled
        KOL_norm,
        zealy_users_norm,
        galxe_users_norm,
        gitcoin_contributors_norm,
        poolcleaners_norm,
        SKY_norm
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

    # Round down the tokens
    def _adjust_tokens_number(tokens: float) -> str:
        raw_number_of_tokens = decimal.Decimal(str(tokens)) * decimal.Decimal(10 ** 18)
        rounded_number_of_tokens = raw_number_of_tokens.quantize(
            decimal.Decimal('1.'),
            rounding=decimal.ROUND_DOWN
        )
        return rounded_number_of_tokens.to_eng_string()

    fourth_dist = {
        address: _adjust_tokens_number(tokens)
        for address, tokens in total_tokens.items()
    }

    # Uncomment this part to save prelims to csv
    res_df = pd.DataFrame({'address': fourth_dist.keys(), 'tokens': fourth_dist.values()})
    res_df['tokens'] = res_df['tokens'].map(lambda x: int(x) / 10 ** 18)
    res_df = res_df.sort_values('tokens', ascending = False)
    res_df.to_csv("prelim_round_4.csv", index = False)

    # Load second distribution
    with open('third_distribution_calculated.json', 'r') as infile:
        third_dist = {
            x['address']: x['amount'] for x in json.load(infile)
        }

    # Combine current airdrop with previous
    total_tokens_combined = {
        k: int(third_dist.get(k, 0)) + int(fourth_dist.get(k, 0))
        for k in set(third_dist) | set(fourth_dist)
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
    open('fourth_distribution_calculated.json', 'w+').write(json.dumps(final_json))


if __name__ == '__main__':
    get_token_distribution_round_4()
