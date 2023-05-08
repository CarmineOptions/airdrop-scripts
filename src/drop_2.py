
'''
Increase tokens of these guys

    df.address = df.address.replace(
        '0x2162FEB49E9Efe2506DE3273f4edabe09d36cbAf'.lower(),
        '0x7657EEb175A5d3B51c5abFa2cd73B367da8F0Ebc4b3a7c1804F77e8b30b1ff4'.lower()
    )
    df.address = df.address.replace(
        '0x271933d1DAFFEC39E1E8c805DbAFf4e10eCd00BB'.lower(),
        '0x6E7B39f21c1A73A2a266A2A60Ac7FDA4AFE6EbE575bA489c87F68A419EdcA81'.lower()
    )
    df.address = df.address.replace(
        '0x5025917a621e5CD46824350ba98F9766160d84BC'.lower(),
        '0x27495304ed75F5257EC68e053e13B4B842Ec9AE65b4720e2EE88b31ecC37A71'.lower()
    )
there was a bug in the contributions... 
df = df[df['Mainnet (StarkNet) address'].map(len) > 42]
was used before the replacement
'''

'''
give some tokens to puddington#8374, he was doing the sybil filtering for airdrop 1, for the tweets
'''
