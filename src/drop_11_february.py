from src.utils import calculate_token_distribution


ROUND = 11
TOTAL_DISTRIBUTION_FOR_TRADING_ = 0
TOTAL_DISTRIBUTION_FOR_LIQUIDITY_PROVIDERS_ = 0
USER_POINTS_FILE_PATH_ = ''

faulty_addresses = ['0x1']
community = {
    '0x036ee5DEa20B5765F5A4FEb81Bb7B899DEF614eD7C2AF0e0d1E05179e35dbD1C': 3_000_000
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
