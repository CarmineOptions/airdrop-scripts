# As per https://medium.com/@carminefinanceinfo/inside-carmine-options-amm-a-complete-breakdown-of-token-distribution-and-allocation-21a7f75e9bca
# and specifically 
#
# During the first month, 25% of the 3.2 million Carmine tokens (800,000) will be distributed at the end of the four periods.
# Moderators will receive a base payment of 1500 tokens for their work in a given month. In addition, in this round of distribution they will receive 1500 tokens for each month they moderate discussions prior to current period. There may also be bonuses available for those who assist with processing feedback from users
# 312 500 for influencers and partners (list might still grow)
# 187,500 tokens will be allocated to users who tweet about their experiences trading or staking on Carmine Options AMM. If you would like to participate, simply tweet your experience using the format “I traded on @CarmineOptions AMM and the experience was …” or “I staked on @CarmineOptions AMM and my experience was …”. To ensure that we don’t miss any tweets, please fill out the following form.
# 125 000 for contributors (graphics, etc). If you contributed, please fill this form.
# 125 000 for media articles/support. If you contributed, please fill this form.
# The remaining Carmine tokens will be allocated towards software development help. This section may increase community spending at the expense of future periods.

# We also manually took care of multiaccounts (sybil attacks). Sadly to were not able to do this accross all sections, just few :/

from typing import Dict
import pandas as pd


def get_moderators() -> Dict[str, float]:
    # Done manually for January till April
    return {
        '0x1': 6000,
        '0x2': 9000,
        '0x3': 9000,
        '0x4': 7500,
        '0x5': 3000,
        '0x6': 4500,
        '0x7': 1500,
        '0x8': 6000
    }


def get_influencers_and_partners() -> Dict[str, float]:
    # 312 500 for influencers and partners (list might still grow)
    # Done manually
    return {
        '0x048df7F681Ee077C3F64eF4E5D8b4f3CCBE5A9Fb57f381b05588aF6b8Bf0fF81': 123,
        '0x06b607099De71297D60A5998c12DA7799132B5C44Eb6B380bE7ad2C733a55054': 123,
        '0x0428c240649b76353644faF011B0d212e167f148fdd7479008Aa44eEaC782BfC': 123,
        '0x0718505b87b5a448205ae22ac84a21b9e568b532ed95285c4c03973f8b1a73e8': 123,
        '0x02356b628D108863BAf8644c945d97bAD70190AF5957031f4852d00D0F690a77': 123
    }


def get_tweeting() -> Dict[str, float]:
    # 187,500 tokens will be allocated to users who tweet about their experiences trading or staking on Carmine Options AMM
    df = pd.read_csv('src/community_projects/tweets_about_using_Mainnet_reviewed.csv')
    addresses = df[~df['Real/Bot'].isin({'Bot', 'Bot '})]['Mainnet address to be rewarded'].to_list()
    addresses = [hex(int(address, 0)) for address in addresses]
    tokens_per_user = 187_500 / len(addresses)
    return {address: tokens_per_user for address in addresses}


def get_contributors() -> Dict[str, float]:
    # 125 000 for contributors (graphics, etc)
    # plus
    # 125 000 for media articles/support

    df = pd.read_csv('src/community_projects/Contributions.csv', sep=';')
    df = df[['Mainnet (StarkNet) address', 'How did you contribute?', 'POINTS', 'NOTES']]
    df = df[~df.POINTS.isin({'0', 'same as number 39', 'same as 49', 'same as 52'})].dropna(subset=['POINTS'])
    df.POINTS = df.POINTS.astype(int)
    df['Mainnet (StarkNet) address'] = df['Mainnet (StarkNet) address'].replace(
        'Starknet Mainnet Address: 0x003b4635841fD07ddC35E79c9844385874d478ACD1127cCD71E975d6EB8304a6',
        '0x003b4635841fD07ddC35E79c9844385874d478ACD1127cCD71E975d6EB8304a6'
    )
    df['Mainnet (StarkNet) address'] = df['Mainnet (StarkNet) address'].map(lambda x: hex(int(x, 0)))
    points = df.set_index('Mainnet (StarkNet) address').POINTS
    points = points.groupby(points.index).sum()
    total_points = points.sum()
    user_tokens = points * 250_000 / total_points
    
    return user_tokens.to_dict()



def get_community_projects(period: str) -> Dict[str, float]:
    if period != 'week_1_4':
        raise ValueError

    influencers_and_partners = get_influencers_and_partners()
    tweeting = get_tweeting()
    contributors = get_contributors()

    # sum everything
    total_tokens = {
        k: influencers_and_partners.get(k, 0) + tweeting.get(k, 0) + contributors.get(k, 0)
        for k in set(influencers_and_partners) | set(tweeting) | set(contributors)
    }

    return total_tokens
