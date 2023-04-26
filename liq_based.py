import requests
import json
import pandas as pd
import time

# int(datetime.datetime(2023, 4, 23, 23, 59, 59).strftime('%s')) + 2*3600
START = 1682294399
END = START + 7 * 24 * 3600
TOKENS_DISTRIBUTED = 125_000

r = requests.get("https://api.carmine.finance/api/v1/mainnet/all-transactions")
data = r.json()
print('State of the download of data: ', data['status'])
print('Number of observations: ', data['length'])


df = pd.DataFrame(
    [x for x in data['data'] if x['action'] in {'WithdrawLiquidity', 'DepositLiquidity'}]
).drop('option', axis = 1)

df['tokens_minted'] = df['tokens_minted'].map(lambda x: int(x, 16) / 10**18)
df['tokens_minted'] = df.apply(
    lambda x: x['tokens_minted'] * (-1) if x['action'].lower() == 'withdrawliquidity' else x['tokens_minted'], axis = 1
)
df = df.sort_values('timestamp')

df = df[~df['caller'].isin({
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


call_pool = df[df['liquidity_pool'] == "Call"].copy().reset_index(drop = True)
put_pool = df[df['liquidity_pool'] == "Put"].copy().reset_index(drop = True)


def get_token_share(df: pd.DataFrame, START: int, END: int, TOKENS_DISTRIBUTED: int) -> pd.DataFrame:
    res = []

    # Iterate over callers
    for user in df['caller'].unique():
        tmp = df[df['caller'] == user].copy()

        # Calculate cumulative sum of tokens minted
        tmp['minted_cum'] = tmp['tokens_minted'].cumsum() 
        # Drop redundant collumns
        tmp = tmp.drop(['action', 'capital_transfered', 'liquidity_pool', 'tokens_minted'], axis = 1)
        
        # Since there is possibility that the user had sth staked before selected period,
        # new row is added at the begining of the period(if it's not already there)
        # and then ffilled, so it takes on the previous value
        # This is done so that information about previous deposit is stored and not lost
        # when slicing df on timestamp
        if START not in list(tmp['timestamp']):
            new_rows = [
                {'timestamp': START, 'caller': user, 'minted_cum' : None}
            ]
            tmp = pd.concat([tmp, pd.DataFrame(new_rows)]).reset_index(drop=True).sort_values('timestamp')
            tmp['minted_cum'] = tmp['minted_cum'].fillna(method = 'ffill')

        # Select period
        tmp = tmp[(tmp['timestamp'] >= START) & (tmp['timestamp'] <= END)]

        # Store caller with minimal minted if it's not zero
        if tmp['minted_cum'].min() > 0:
            res.append(
                {'caller': user, 'min_minted_cum': tmp['minted_cum'].min()}
            )


    res = pd.DataFrame(res).sort_values('min_minted_cum', ascending = False).reset_index(drop = True)
    res['share'] = res['min_minted_cum'] / res['min_minted_cum'].sum()
    res['share_tokens'] = res['share'] * TOKENS_DISTRIBUTED
    return res

call_res = get_token_share(call_pool, START, END, TOKENS_DISTRIBUTED)
put_res = get_token_share(put_pool, START, END, TOKENS_DISTRIBUTED)

call_res['caller_short'] = call_res['caller'].map(lambda x: x[:5] + '...' + x[-3:])
put_res['caller_short'] = put_res['caller'].map(lambda x: x[:5] + '...' + x[-3:])

print(f"Eligible for volume-based airdrop call {len(call_res)}")
print(f"Eligible for volume-based airdrop put {len(put_res)}")

print('\n' * 3)

print("\033[94m CALL RESULTS \033[0m")
for i in range(len(call_res)):
     print(call_res.loc[i, 'caller_short'], '   ', round(call_res.loc[i, 'share_tokens'], 2))

print('\n' * 3)

print("\033[94m PUT RESULTS \033[0m")
for i in range(len(put_res)):
     print(put_res.loc[i, 'caller_short'], '   ', round(put_res.loc[i, 'share_tokens'], 2))



