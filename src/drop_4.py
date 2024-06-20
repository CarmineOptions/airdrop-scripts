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
TOKENS_PER_TESTNET_CONTRIBUTOR = 40.0
TOKENS_PER_OG_CONTRIBUTOR = 100.0


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
        "allocated for points": 8_000_000,
        "Community devs (DeRisk)": 200_000,
        "Community devs (Konoha)": 200_000
    }

    # Lead ambassadors, ambassadors, moderators, investors
    lead_ambassadors = {
        '0x018D4756921D34b0026731F427C6b365687Ce61CE060141Bf26867f0920D2191': 225_000,
        '0x01fb62ac54f9fa99e1417f83bcb88485556427397f717ed4e7233bc99be31bff': 225_000,
        '0x054e0ab67bd384312d640915b55d7e918fe2031269ec26f8fc7fde9abbd1e0a5': 175_000
    }
    ambassadors_norm = normalize_addresses_in_map(lead_ambassadors)

    moderators = {
        '0x039e14d815587cdd5ae400684e5d60848d9a134b378260cc1f2de6e7aedcdb45': 87_500,
        '0x0639F7aD800Fcbe2aD56E3b000f9A0581759CcE989b3Ee09477055c0816A12c7': 70_000,
        '0x053eAD44Bb90853003d70E6930000Ef8C4a4819493fDC8f1CbdC1282121498eC': 52_500
    }
    moderators_norm = normalize_addresses_in_map(moderators)

    ambassadors_f = {
        '0x04a8713ab7aff5e97fb1aa7652314a5ed6102b200da75ef42078a5a01fef4093': 89_859,
        '0x00aa7fe49a402af47bf2bcfee7e356a5ae18db0adedaa2c44a1de60c6ef9caef': 31_525,
        '0x0558808A3C00c778C93E3d4348687b048613993E6b03836726B5d581f9960515': 101_577,
        '0x000928e2956ad7138c273120412bf2283d83e985b2426c2b8ddf146fd6b37884': 41_072,
        '0x02ba1c396a2a3bd5dcc62fe3f9bd9f85eaa6580609bb903ccbb8aad374cf3f76': 74_139,
        '0x05bb61ab3472556d0151bb4fa22e3514d1a490cb31229b7bcca33744afd5858f': 44_921,
        '0x046d95a7f86ec19412a4da5d28f6a6addf62f1cd2c5d0defbe18bff1d96a2458': 0,
        '0x049c691d23cf572e3318472dac01d5a6d996470aa1050af0ccadda392c073efb': 64_270,
        '0x00a975351cf03ad81d5d08f953dcc415da07012ff6d2d44a074c384feb0db35d': 29_201,
        '0x06Ae3E526C67A3f38393034abAC34E8274A5683c2c4f00D6aeFEa98057daE5Af': 42_903,
        '0x055f973e925Fba11C9cEA1565ff000f196a7DdfCb73c7292774a8d5408FA6bF4': 43_870,
        # 'ak': 36_663  # get next token allocation if provide the address
    }
    ambassadors_f_norm = normalize_addresses_in_map(ambassadors_f)

    # investors
    investors = {
        '0x05a4523982b437aadd1b5109b6618c46f7b1c42f5f9e7de1a3b84091f87d411b': 3_000_000,
        '0x01d54e7bb22bdaf09bea5a05781d861c97cd6edeb84abd6714db69d6036856d3': 2_500_000,
        '0x056d761e1e5d1918dba05de02afdbd8de8da01a63147dce828c9b1fe9227077d': 14_500_000  # multisig
    }
    investors_norm = normalize_addresses_in_map(investors)

    # KOL
    KOL = {
        '0x04e7F967f9b075D309E052f2Ac0d9A2F5a6DcD130BFe6e8906A84b3BE7104529': 16_000,
        '0x07Ba5bA6F3146E5715452339Ec8871bAD3d991686A042dBCEcEdC5a6e103Ae5b': 12_000,
        '0x0672E2d7E07A07d9aE1F3E080B7aB6e5aa1B6a30192E021A0F7614ec698e1fEd': 18_000
    }
    KOL_norm = normalize_addresses_in_map(KOL)

    # Core Team
    core_team = {
        '0x00d79a15d84f5820310db21f953a0fae92c95e25d93cb983cc0c27fc4c52273c': 7_001_443,
        # 'm': 0,  # went to multisig
        '0x06e2c2a5da2e5478b1103d452486afba8378e91f32a124f0712f09edd3ccd923': 2_774_035,
        '0x03d1525605db970fa1724693404f5f64cba8af82ec4aab514e6ebd3dec4838ad': 1_818_602,
        '0x062c290f0afa1ea2d6b6d11f6f8ffb8e626f796e13be1cf09b84b2edaa083472': 116_389,
        '0x06717eaf502baac2b6b2c6ee3ac39b34a52e726a73905ed586e757158270a0af': 1_664_844,
        '0x07fce7a88b861dfea6af35d16cd60f4ea3bba98dc7b596d4ca529b6c182fd3fd': 417_600,
        '0x022eb3aDCF35A52Cb39c9F35177176dEDa69Ed323c57D3eC409dd268664D18DF': 111_385,
        '0x0446e7774b852215e81f09a6ec01b9da92e34a1c64fda5e627d492fd07cb6306': 128_943,
        '0x05105649f42252f79109356e1c8765b7dcdb9bf4a6a68534e7fc962421c7efd2': 210_101,
        '0x06c59d2244250f2540a2694472e3c31262e887ff02582ef864bf0e76c34e1298': 57_795,
        '0x0528f064c43e2d6Ee73bCbfB725bAa293CD31Ea1f1861EA2F80Bc283Ea4Ad728': 120_614,
        '0x00777558f1c767126461540d1f10118981d30bd620707e99686bfc9f00ae66f0': 4_123,
        '0x0244dda2c6581eb158db225992153c9d49e92c412424daeb83a773fa9822eeef': 3_352_361  # multisig
    }
    core_team_norm = normalize_addresses_in_map(core_team)

    # user points
    user_points = pd.read_csv(USER_POINTS_FILE_PATH)
    user_points['user_points_total'] = user_points.apply(lambda x: (
            x.trading_points * TRADING_MULTIPLIER + x.liquidity_points * LIQUIDITY_MULTIPLIER
            + x.referral_points * REFERRAL_MULTIPLIER + x.vote_points * VOTE_MULTIPLIER
    ), axis=1)
    user_points.user_address = user_points.user_address.apply(lambda x: normalize_sn_address(x))
    tokens_per_point = distribution_model["allocated for points"] / user_points.user_points_total.sum()
    user_points['user_tokens'] = user_points.user_points_total * tokens_per_point
    print(f"Tokens for user points: {user_points['user_tokens'].sum()}")

    assert len(user_points.user_address.unique()) == user_points.shape[0], "Addresses for timestamp are not unique"
    user_points_norm = {row.user_address: row.user_tokens for _, row in user_points.iterrows()}

    # f.s.users
    fsusers = {
        '0x00a975351cf03ad81d5d08f953dcc415da07012ff6d2d44a074c384feb0db35d': 7_500,
        '0x04303Ef08A7e078bc867a745aEE5fa9DEf4fAF56643bd933D85C0717042e0CDc': 40_000,
        '0x039e14d815587cdd5ae400684e5d60848d9a134b378260cc1f2de6e7aedcdb45': 12_500
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
        '0x0365421f66a3fb7630ac030fb83a1db5078bfe29cc22f27f95a9978ff9ab7b6e': 30
    }

    total_days = sum(konoha_contributor_days.values())

    total_tokens_allocated = distribution_model["Community devs (Konoha)"]
    allocation_per_day = total_tokens_allocated / total_days
    konoha_contributors = {address: allocation_per_day * days for address, days in konoha_contributor_days.items()}
    konoha_contributors_norm = normalize_addresses_in_map(konoha_contributors)

    # testnet_contributors
    testnet_addresses = extract_starknet_addresses(TESTNET_USERS_FILE_PATH)
    testnet_addresses = {normalize_sn_address(address) for address in testnet_addresses}
    token_per_testnet_contributor = TOKENS_PER_TESTNET_CONTRIBUTOR
    testnet_contributors_norm = {
        address: token_per_testnet_contributor for address in testnet_addresses
    }
    print(f"Tokens for testnet users: {sum(testnet_contributors_norm.values())}")

    # OG contributors
    og_user_addresses = extract_starknet_addresses(OG_USERS_FILE_PATH)
    og_user_addresses = {normalize_sn_address(address) for address in og_user_addresses}
    token_per_og_contributor = TOKENS_PER_OG_CONTRIBUTOR
    og_contributors_norm = {
        address: token_per_og_contributor for address in og_user_addresses
    }
    print(f"Tokens for OG users: {sum(og_contributors_norm.values())}")

    all_contributor_maps = [
        core_team_norm,
        ambassadors_norm,
        moderators_norm,
        ambassadors_f_norm,
        investors_norm,
        user_points_norm,
        konoha_contributors_norm,
        derisk_contributors_norm,
        og_contributors_norm,
        testnet_contributors_norm,
        fsusers_norm,
        KOL_norm
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

    fourth_dist = {
        address: _adjust_tokens_number(tokens)
        for address, tokens in total_tokens.items()
    }

    # exclude faulty addresses
    faulty_addresses = ['0x84e33438bb816f1daec2b70b0ba9da85fddc6e962ccea186d073e9a0f2e56a5b']
    for address in faulty_addresses:
        del fourth_dist[address]

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
