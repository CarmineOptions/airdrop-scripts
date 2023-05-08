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


def get_moderators_and_community_devs() -> Dict[str, float]:
    # Done manually for January till April
    '''
    Community devs:
    0x0486deba6028c880ce3d1730a4496e4f12d7b813367d43510ea410f5ff7e3efb: 11250
    0x0365421f66a3fb7630ac030fb83a1db5078bfe29cc22f27f95a9978ff9ab7b6e: 11250
    - 3750 will be distributed to each of them for "week 5", week 6-8 has to be agreed

    Moderators
    0x04d2FE1Ff7c0181a4F473dCd982402D456385BAE3a0fc38C49C0A99A620d1abe: 6000
    0x039e14d815587cdd5ae400684e5d60848d9a134b378260cc1f2de6e7aedcdb45: 9000
    wallet?		9000
    0x006a0f490289fe04ea6ba158ed5fd3339628832432d7bc802941664843bc904f: 7500
    0x04d3E6A312d4089Ac798Ae3Cf5766AdB1c1863E23222B5602F19682E08DB2Bd1: 3000
    wallet?		4500
    0x06E7B39f21c1A73A2a266A2A60Ac7FDA4AFE6EbE575bA489c87F68A419EdcA81: 1500
    0x053eAD44Bb90853003d70E6930000Ef8C4a4819493fDC8f1CbdC1282121498eC: 6000
    '''
    return {
        # Community devs:
        '0x486deba6028c880ce3d1730a4496e4f12d7b813367d43510ea410f5ff7e3efb': 11250,
        '0x365421f66a3fb7630ac030fb83a1db5078bfe29cc22f27f95a9978ff9ab7b6e': 11250,

        # Moderators
        '0x4d2FE1Ff7c0181a4F473dCd982402D456385BAE3a0fc38C49C0A99A620d1abe': 6000,
        '0x39e14d815587cdd5ae400684e5d60848d9a134b378260cc1f2de6e7aedcdb45': 9000,
        # wallet?		9000
        '0x6a0f490289fe04ea6ba158ed5fd3339628832432d7bc802941664843bc904f': 7500,
        '0x4d3E6A312d4089Ac798Ae3Cf5766AdB1c1863E23222B5602F19682E08DB2Bd1': 3000,
        # wallet?		4500
        '0x6E7B39f21c1A73A2a266A2A60Ac7FDA4AFE6EbE575bA489c87F68A419EdcA81': 1500,
        '0x53eAD44Bb90853003d70E6930000Ef8C4a4819493fDC8f1CbdC1282121498eC': 6000,
    }


def get_influencers_and_partners() -> Dict[str, float]:
    '''
    # 312 500 for influencers and partners (12 in total, 26041 to each)
    # Done manually
    '''
    return {
        '0x48df7F681Ee077C3F64eF4E5D8b4f3CCBE5A9Fb57f381b05588aF6b8Bf0fF81': 26041,
        '0x6b607099De71297D60A5998c12DA7799132B5C44Eb6B380bE7ad2C733a55054': 26041,
        '0x428c240649b76353644faF011B0d212e167f148fdd7479008Aa44eEaC782BfC': 26041,
        '0x718505b87b5a448205ae22ac84a21b9e568b532ed95285c4c03973f8b1a73e8': 26041,
        '0x2356b628D108863BAf8644c945d97bAD70190AF5957031f4852d00D0F690a77': 26041,
        '0x284a1ad6382cffc520d8f711cf9519ccf43b3c105b89ef081cbe1a625322410': 26041,
        '0x47379D56D006a6A899b220094721F777C8d9f24ebB17ff83AC01310d6178b3f': 26041,
        '0x640cC5d7E32Bb5226E49A1c41b697dA98962E66a86f6F109A089c8291E3BF40': 26041,
        '0x11cebe36f313388a167a18a1669f35dd47c459fdde1d350c6249fcbc8aa6894': 26041,
        '0x59e0EE330B5e0aedA59faA27e5a09ae9fDD60fB25DE9BC8410b0F36052096D7': 26041,
        '0x9fe5c33f289774721333ddd3ec6a434afff5891c89e2b90fe64aee3e9c3711': 26041,
        '0x1Ba0972858F4068Bd14C951C853a204F78D672f28f4d2ABe757674DdB7ebc9C': 26041,
    }


def get_tweeting() -> Dict[str, float]:
    # 187,500 tokens will be allocated to users who tweet about their experiences trading or staking on Carmine Options AMM
    df = pd.read_csv('src/community_projects/tweets_about_using_Mainnet_reviewed.csv')
    addresses = df[~df['Real/Bot'].isin({'Bot', 'Bot ', 'Double posted'})]['Mainnet address to be rewarded'].to_list()
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
    df = df[df['Mainnet (StarkNet) address'].map(len) > 42]
    points = df.set_index('Mainnet (StarkNet) address').POINTS
    points = points.groupby(points.index).sum()
    total_points = points.sum()
    user_tokens = points * 250_000 / total_points
    
    return user_tokens.to_dict()



def get_community_projects(period: str) -> Dict[str, float]:
    if period != 'week_1_4':
        raise ValueError

    moderators_and_community_devs = get_moderators_and_community_devs()
    influencers_and_partners = get_influencers_and_partners()
    tweeting = get_tweeting()
    contributors = get_contributors()

    # sum everything
    total_tokens = {
        k: influencers_and_partners.get(k, 0) + tweeting.get(k, 0) + contributors.get(k, 0) + moderators_and_community_devs.get(k, 0)
        for k in set(influencers_and_partners) | set(tweeting) | set(contributors) | set(moderators_and_community_devs)
    }

    return total_tokens
