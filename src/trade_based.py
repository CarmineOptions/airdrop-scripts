# Script for generating list of Trading based rewards

from typing import Dict, List, Set
import requests
import pandas as pd


def get_traders_drop(
    start: int,
    end: int,
    tokens_distributed: int,
    core_team_addresses: Set[str]
) -> Dict[str, float]:
    # Fetch data from carmine database
    # The database stores all Trade and Liquidity events - 
    # TradeOpen, TradeClose, TradeSettle, DepositLiquidity, WithdrawLiquidity
    r = requests.get("https://api.carmine.finance/api/v1/mainnet/all-transactions")
    data = r.json()
    print('State of the download of data: ', data['status'])
    print('Number of observations: ', data['length'])

    # Select only events related to trading
    df = pd.DataFrame.from_records([x for x in data['data'] if x['action'] in {'TradeClose', 'TradeOpen'}])

    # Expand 'option' collumn into separate collumns 
    df['option_side'] = df['option'].map(lambda x: x['option_side'])
    df['option_type'] = df['option'].map(lambda x: x['option_type'])
    df['strike_price'] = df['option'].map(lambda x: int(x['strike_price'], 0)) / 2**61
    df['capital_transfered'] = df['capital_transfered'].map(lambda x: int(x, 0))
    df['tokens_minted'] = df['tokens_minted'].map(lambda x: int(x, 0))

    # Select only relevant collumns
    df = df[['timestamp', 'caller', 'capital_transfered', 'tokens_minted', 'option_side', 'option_type', 'strike_price']]
    # Select entries for given period
    df = df[(df['timestamp'] >= start) & (df['timestamp'] <= end)]

    # Function from calculating premia from transaction info
    def calc_premium(row: pd.Series) -> float:
        if row['option_side'] == 0:  # long
            # Returned in decimals of that given currency
            return row['capital_transfered']
        # Short
        if row['option_type'] == 0:  # call
            return row['tokens_minted'] - row['capital_transfered']
        # Short and Put
        # The row.tokens_minted has 18 decimals, divided it give option size
        # The row.tokens_minted / 10**18 multiplied by the strike gives the amount of cash locked
        # row.tokens_minted / 10**18 * row.strike_price multiplied by 10**6 puts in the same decimals as the capital transfered
        # capital transfered has 6 (USDC)
        return row['tokens_minted'] / 10**18 * row['strike_price'] * 10**6 - row['capital_transfered']

    # Calculate premia
    df['premium'] = df.apply(calc_premium, axis = 1)

    # Standardize addresses
    df['caller'] = df.caller.map(lambda x: hex(int(x, 0)))

    # Remove any entries from core team wallets
    # But first normalize core_team_addresses as well
    core_team_addresses = {hex(int(x, 0)) for x in core_team_addresses}
    df = df[~df.caller.isin(core_team_addresses)]

    # Separate data into call and put options
    call_distribution = df[df['option_type'] == 0]
    put_distribution = df[df['option_type'] == 1]

    # Aggregate premia over unique adresses and calculate number of tokens that belong to the user
    results_call_premia = call_distribution.groupby('caller')['premium'].sum()
    results_call = results_call_premia / results_call_premia.sum() * tokens_distributed
    # results_call.index = results_call.index.map(lambda x: x[:5] + '...' + x[-3:])
    # results_call = results_call.sort_values(ascending=False)

    results_put = put_distribution.groupby('caller')['premium'].sum()
    results_put = results_put / results_put.sum() * tokens_distributed
    # results_put.index = results_put.index.map(lambda x: x[:5] + '...' + x[-3:])
    # results_put = results_put.sort_values(ascending=False)

    # # Print results
    # print(f"Period start: {pd.to_datetime(start, unit='s')}")
    # print(f"Period end: {pd.to_datetime(end, unit='s')}")
    # print(f"Eligible for volume-based airdrop call {len(results_call)}")
    # print(f"Eligible for volume-based airdrop put {len(results_put)}")

    # print('\n' * 3)

    # print("\033[94m CALL RESULTS \033[0m")
    # for i in range(len(results_call)):
    #     print(results_call.index[i], '   ', round(results_call.iloc[i], 2))

    # print('\n' * 3)

    # print("\033[94m PUT RESULTS \033[0m")
    # for i in range(len(results_put)):
    #     print(results_put.index[i], '   ', round(results_put.iloc[i], 2))

    # print('\n' * 3)

    # total_call_premium = call_distribution['premium'].sum()
    # total_put_premium = put_distribution['premium'].sum()

    # print("Total value of all premia traded in calls: {:.2f} ETH".format(total_call_premium/10**18))
    # print("Total value of all premia traded in puts: {:.2f} USDC".format(total_put_premium/10**6))

    total_tokens = pd.concat([results_call, results_put])
    total_tokens = total_tokens.groupby(total_tokens.index).sum()

    return total_tokens.to_dict()
