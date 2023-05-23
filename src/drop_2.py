
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


'''
https://github.com/CarmineOptions/carmine-protocol/commit/c513ec2c672c10c13f50ecece0cd216c6493cfcc#diff-770ea621de180501274b95ab5d6ac3225b418be5801a8e10bc11210d6f0250f7R8
has to be updated... ie user can claim "get_eligible_amount minus airdrop_claimed"
'''

'''
the json generated from this script will collect both the numbers already written into smart contract
(first_distribution_calculated.json) plus the numbers from this script
'''

'''
periods end with 4th June -> 5th June there will be proposal for the distribution
'''

'''
watch out for tokens, since int is not precise enough... so you have to use decimals

Additional tokens:
александр gets 3kCARM to  wallet 0x068C8E344aBF736892a97daC9a3daF2952A047b769E085D7557901Ddf31a435f... for sharing info about us in his discord (roughly 12k followers, looks like interesting engagement, good feedback)
 
Our team
Presto
'''



