from src.utils import calculate_token_distribution


ROUND = 11
TOTAL_DISTRIBUTION_FOR_TRADING_ = 183_838
TOTAL_DISTRIBUTION_FOR_LIQUIDITY_PROVIDERS_ = 122_185
USER_POINTS_FILE_PATH_ = 'src/allocation_eleven/user-points.csv'

faulty_addresses = ['0x1']
community = {
    '0x050c439fCfA077cd4a1ff4477C5242D4781010D9B1C0f1e2a96980896eD63A38': 2200,
    '0x00a975351cf03ad81d5d08f953dcc415da07012ff6d2d44a074c384feb0db35d': 2200
}


if __name__ == '__main__':
    calculate_token_distribution(
        round_number=ROUND,
        total_distribution_for_trading=TOTAL_DISTRIBUTION_FOR_TRADING_,
        total_distribution_for_liquidity_providers=TOTAL_DISTRIBUTION_FOR_LIQUIDITY_PROVIDERS_,
        user_points_file_path=USER_POINTS_FILE_PATH_,
        community_distr=community,
        faulty_address_list=faulty_addresses
    )
