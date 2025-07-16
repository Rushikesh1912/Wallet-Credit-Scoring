import numpy as np
import pandas as pd


def extract_features(wallet_id, txns):
    actions = [txn['action'].lower() for txn in txns]
    timestamps = [int(txn['timestamp']) for txn in txns]

    amounts = []
    for txn in txns:
        try:
            amt = float(txn.get('actionData', {}).get('amount', 0))
            amounts.append(amt)
        except (ValueError, TypeError):
            amounts.append(0)

    num_deposit = actions.count('deposit')
    num_borrow = actions.count('borrow')
    num_repay = actions.count('repay')
    num_liquidation = actions.count('liquidationcall')
    num_redeem = actions.count('redeemunderlying')

    repay_ratio = num_repay / num_borrow if num_borrow else 0
    total_amount = sum(amounts)
    avg_amount = np.mean(amounts) if amounts else 0
    avg_gap = np.mean(np.diff(sorted(
        timestamps))) if len(timestamps) > 1 else 0

    num_unique_actions = len(set(actions))
    liquidation_rate = num_liquidation / (num_borrow + 1)

    return {
        'wallet_id': wallet_id,
        'num_deposit': num_deposit,
        'num_borrow': num_borrow,
        'num_repay': num_repay,
        'num_liquidation': num_liquidation,
        'num_redeem': num_redeem,
        'repay_ratio': repay_ratio,
        'total_amount': total_amount,
        'avg_amount': avg_amount,
        'avg_time_gap': avg_gap,
        'num_unique_actions': num_unique_actions,
        'liquidation_rate': liquidation_rate
    }


def process_all_wallets(data):
    records = []
    for wallet_id, txns in data.items():
        features = extract_features(wallet_id, txns)
        records.append(features)
    return pd.DataFrame(records)
