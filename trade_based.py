# Done by Marek in https://discord.com/channels/969228248552706078/1045794107760574475/1097629679504085076

import requests
import json
import pandas as pd

r = requests.get("https://api.carmine.finance/api/v1/mainnet/all-transactions")
data = r.json()
print('State of the download of data: ', data['status'])
print('Number of observations: ', data['length'])

df = pd.DataFrame.from_records([x for x in data['data'] if x['action'] in {'TradeClose', 'TradeOpen'}])
df['option_side'] = df['option'].map(lambda x: x['option_side'])
df['option_type'] = df['option'].map(lambda x: x['option_type'])
df['strike_price'] = df['option'].map(lambda x: int(x['strike_price'], 0)) / 2**61
df['capital_transfered'] = df['capital_transfered'].map(lambda x: int(x, 0))
df['tokens_minted'] = df['tokens_minted'].map(lambda x: int(x, 0))
# df['strike_price'] = df['strike_price'].map(lambda x: int(x, 0))
df = df[['timestamp', 'caller', 'capital_transfered', 'tokens_minted', 'option_side', 'option_type', 'strike_price']]
df = df[df['timestamp'] < 1681689599]

def calc_premium(row: pd.Series) -> float:
    if row['option_side'] == 0:  # long
        # returned in decimals of that given currency
        return row['capital_transfered']
    # short
    if row['option_type'] == 0:  # call
        return row['tokens_minted'] - row['capital_transfered']
    # short and put
    # the row.tokens_minted has 18 decimals, divided it give option size
    # the row.tokens_minted / 10**18 multiplied by the strike gives the amount of cash locked
    # row.tokens_minted / 10**18 * row.strike_price multiplied by 10**6 puts in the same decimals as the capital transfered
    # capital transfered has 6 (USDC)
    return row['tokens_minted'] / 10**18 * row['strike_price'] * 10**6 - row['capital_transfered']
df['premium'] = df.apply(calc_premium, axis = 1)

df = df[~df.caller.isin({
    '0x0583a9d956d65628f806386ab5b12dccd74236a3c6b930ded9cf3c54efc722a1',
    '0x583a9d956d65628f806386ab5b12dccd74236a3c6b930ded9cf3c54efc722a1',
    '0x06717eaf502baac2b6b2c6ee3ac39b34a52e726a73905ed586e757158270a0af',
    '0x6717eaf502baac2b6b2c6ee3ac39b34a52e726a73905ed586e757158270a0af',
    '0x0011d341c6e841426448ff39aa443a6dbb428914e05ba2259463c18308b86233',
    '0x011d341c6e841426448ff39aa443a6dbb428914e05ba2259463c18308b86233',
    '0x11d341c6e841426448ff39aa443a6dbb428914e05ba2259463c18308b86233',
    '0x03d1525605db970fa1724693404f5f64cba8af82ec4aab514e6ebd3dec4838ad',
    '0x3d1525605db970fa1724693404f5f64cba8af82ec4aab514e6ebd3dec4838ad',
    '0x03c032b19003Bdd6f4155a30FFFA0bDA3a9cAe45Feb994A721299d7E5096568c',
    '0x3c032b19003Bdd6f4155a30FFFA0bDA3a9cAe45Feb994A721299d7E5096568c',
})]

call_distribution = df[df['option_type'] == 0]
put_distribution = df[df['option_type'] == 1]
results_call_premia = call_distribution.groupby('caller')['premium'].sum()
results_call = results_call_premia / results_call_premia.sum() * 125000
results_call.index = results_call.index.map(lambda x: x[:5] + '...' + x[-3:])
results_put = put_distribution.groupby('caller')['premium'].sum()
results_put = results_put / results_put.sum() * 125000
results_put.index = results_put.index.map(lambda x: x[:5] + '...' + x[-3:])
results_call = results_call.sort_values(ascending=False)
results_put = results_put.sort_values(ascending=False)

print(f"Eligible for volume-based airdrop call {len(results_call)}".format())
print(f"Eligible for volume-based airdrop put {len(results_put)}".format())

for i in range(len(results_call)):
     print(results_call.index[i], '   ', round(results_call.iloc[i], 2))

total_call_premium = call_distribution['premium'].sum()
total_put_premium = put_distribution['premium'].sum()

print("Total value of all premia traded in calls: {:.2f} ETH".format(total_call_premium/10**18))
print("Total value of all premia traded in puts: {:.2f} USDC".format(total_put_premium/10**6))
